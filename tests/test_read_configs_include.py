import io
import os
import tempfile
import pytest
import subprocess

ENV_SPLIT_STR: str = "#env for testing#"


@pytest.fixture(scope="module")
def root_dir(request):
    return os.path.dirname(os.path.dirname(request.fspath))


@pytest.fixture(scope="function")
def run_in_compose_dir(root_dir):
    compose_dir = os.path.join(root_dir, "birdhouse")
    old_cwd = os.getcwd()
    os.chdir(compose_dir)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@pytest.fixture(scope="module")
def read_config_include_file(root_dir) -> str:
    return os.path.join(root_dir, "birdhouse", "read-configs.include.sh")


@pytest.fixture
def tmp_build_dir():
    with tempfile.TemporaryDirectory() as build_dir:
        yield build_dir


def set_local_env(env_file: io.FileIO, content: str | dict) -> None:
    env_file.truncate()
    if isinstance(content, dict):
        env_file.write("\n".join(f"{k}={v}" for k, v in content.items()))
    else:
        env_file.write(content)


def split_and_strip(s: str, split_on="\n") -> list[str]:
    return [cline for line in s.split(split_on) if (cline := line.strip())]


def get_read_config_stdout(proc: subprocess.CompletedProcess) -> str:
    return proc.stdout.split(ENV_SPLIT_STR)[0]


def get_command_stdout(proc: subprocess.CompletedProcess) -> str:
    return proc.stdout.split(ENV_SPLIT_STR)[1]


class TestReadConfigs:
    test_func: str = " read_components_default_env"

    default_all_conf_order: list[str] = [
        "./config/proxy",
        "./config/canarie-api",
        "./config/geoserver",
        "./config/postgres",
        "./config/wps_outputs-volume",
        "./config/flyingpigeon",
        "./config/finch",
        "./config/raven",
        "./config/data-volume",
        "./config/hummingbird",
        "./config/thredds",
        "./config/portainer",
        "./config/magpie",
        "./config/twitcher",
        "./config/jupyterhub"
    ]

    def run_func(
        self, include_file: str, local_env: str | dict, command_suffix: str = ""
    ) -> subprocess.CompletedProcess:
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
                set_local_env(f, local_env)

            env = {"BIRDHOUSE_LOCAL_ENV": f.name}

            if command_suffix:
                command_suffix = f"&& echo '{ENV_SPLIT_STR}' && {command_suffix}"
            command = f". {include_file} && read_configs {command_suffix}"
            proc = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                universal_newlines=True,
            )
            if proc.returncode:
                raise subprocess.SubprocessError(
                    f"'{command}' failed with return code: {proc.returncode}\nError:\n{proc.stderr}"
                )
            return proc
        finally:
            os.unlink(f.name)

    def test_return_code(self, read_config_include_file) -> None:
        """Test that the return code is 0"""
        proc = self.run_func(read_config_include_file, {})
        assert proc.returncode == 0

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_all_conf_dirs_set(self, read_config_include_file) -> None:
        """Test that the ALL_CONF_DIRS variable is set"""
        proc = self.run_func(read_config_include_file, {}, 'echo "$ALL_CONF_DIRS"')
        print(proc.stdout)  # useful for debugging when assert fail
        assert get_command_stdout(proc).strip()

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_all_conf_dirs_default_order(self, read_config_include_file) -> None:
        """Test that the expected order that default.env files are loaded is correct"""
        proc = self.run_func(read_config_include_file, {}, 'echo "$ALL_CONF_DIRS"')
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc)) == self.default_all_conf_order

    def test_all_conf_dirs_extra_last(self, read_config_include_file) -> None:
        """Test that any extra components are loaded last"""
        extra = {"EXTRA_CONF_DIRS": '"./components/cowbird\n./components/weaver"'}
        proc = self.run_func(read_config_include_file, extra, 'echo "$ALL_CONF_DIRS"')
        assert split_and_strip(get_command_stdout(proc))[-2:] == [
            "./components/cowbird",
            "./components/weaver",
        ]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_dependencies_loaded_first(self, read_config_include_file) -> None:
        """Test that dependencies are loaded first"""
        extra = {"EXTRA_CONF_DIRS": '"./optional-components/test-weaver"'}
        proc = self.run_func(read_config_include_file, extra, 'echo "$ALL_CONF_DIRS"')
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc))[-2:] == [
            "./components/weaver",
            "./optional-components/test-weaver",
        ]

    def test_non_project_components_included(self, read_config_include_file) -> None:
        """Test that extra components can be included"""
        extra = {"EXTRA_CONF_DIRS": '"./blah/other-random-component"'}
        proc = self.run_func(read_config_include_file, extra, 'echo "$ALL_CONF_DIRS"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "./blah/other-random-component"

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_delayed_eval_default_value(self, read_config_include_file) -> None:
        """Test delayed eval when value not set in env.local"""
        extra = {"PAVICS_FQDN": '"fqdn.example.com"'}
        proc = self.run_func(read_config_include_file, extra,
                             'echo "$PAVICS_FQDN_PUBLIC - $JUPYTERHUB_USER_DATA_DIR - $GEOSERVER_DATA_DIR"')
        print(proc.stdout)  # useful for debugging when assert fail
        # By default, PAVICS_FQDN_PUBLIC has same value as PAVICS_FQDN.
        assert (split_and_strip(get_command_stdout(proc))[-1] ==
                "fqdn.example.com - /data/jupyterhub_user_data - /data/geoserver")

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_delayed_eval_custom_value(self, read_config_include_file) -> None:
        """Test delayed eval when value is set in env.local"""
        extra = {"PAVICS_FQDN": '"fqdn.example.com"',
                 "PAVICS_FQDN_PUBLIC": '"public.example.com"',
                 "DATA_PERSIST_ROOT": '"/my-data-root"',  # indirectly change JUPYTERHUB_USER_DATA_DIR
                 "GEOSERVER_DATA_DIR": '"/my-geoserver-data"',
                 }
        proc = self.run_func(read_config_include_file, extra,
                             'echo "$PAVICS_FQDN_PUBLIC - $JUPYTERHUB_USER_DATA_DIR - $GEOSERVER_DATA_DIR"')
        print(proc.stdout)  # useful for debugging when assert fail
        # If PAVICS_FQDN_PUBLIC is set in env.local, that value should be effective.
        assert (split_and_strip(get_command_stdout(proc))[-1] ==
                "public.example.com - /my-data-root/jupyterhub_user_data - /my-geoserver-data")


class TestCreateComposeConfList:
    @staticmethod
    def default_conf_list_order(tmp_build_dir) -> list[str]:
        return [
            f"{tmp_build_dir}/docker-compose.yml",
            f"{tmp_build_dir}/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/canarie-api/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/geoserver/docker-compose-extra.yml",
            f"{tmp_build_dir}/geoserver/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/geoserver/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/postgres/docker-compose-extra.yml",
            f"{tmp_build_dir}/wps_outputs-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/wps_outputs-volume/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/wps_outputs-volume/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/flyingpigeon/docker-compose-extra.yml",
            f"{tmp_build_dir}/flyingpigeon/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/flyingpigeon/config/wps_outputs-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/finch/docker-compose-extra.yml",
            f"{tmp_build_dir}/finch/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/finch/config/wps_outputs-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/raven/docker-compose-extra.yml",
            f"{tmp_build_dir}/raven/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/raven/config/wps_outputs-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/data-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/hummingbird/docker-compose-extra.yml",
            f"{tmp_build_dir}/hummingbird/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/hummingbird/config/data-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/hummingbird/config/wps_outputs-volume/docker-compose-extra.yml",
            f"{tmp_build_dir}/thredds/docker-compose-extra.yml",
            f"{tmp_build_dir}/thredds/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/thredds/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/portainer/docker-compose-extra.yml",
            f"{tmp_build_dir}/portainer/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/geoserver/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/flyingpigeon/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/finch/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/raven/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/hummingbird/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/thredds/config/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/magpie/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/magpie/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/twitcher/docker-compose-extra.yml",
            f"{tmp_build_dir}/twitcher/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/twitcher/config/proxy/docker-compose-extra.yml",
            f"{tmp_build_dir}/jupyterhub/docker-compose-extra.yml",
            f"{tmp_build_dir}/jupyterhub/config/canarie-api/docker-compose-extra.yml",
            f"{tmp_build_dir}/jupyterhub/config/proxy/docker-compose-extra.yml",
        ]

    def run_func(self, include_file: str, local_env: dict, command_suffix: str = "") -> subprocess.CompletedProcess:
        if command_suffix:
            command_suffix = f"&& echo '{ENV_SPLIT_STR}' && {command_suffix}"
        command = f". {include_file} && create_compose_conf_list {command_suffix}"
        proc = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=local_env,
            check=True,
            universal_newlines=True,
        )
        if proc.returncode:
            raise subprocess.SubprocessError(
                f"'{command}' failed with return code: {proc.returncode}\nError:\n{proc.stderr}"
            )
        return proc

    def test_all_conf_dirs_empty(self, read_config_include_file, tmp_build_dir):
        """Test that only the base compose file is used when ALL_CONF_DIRS is empty"""
        proc = self.run_func(read_config_include_file, {"BUILD_DIR": tmp_build_dir}, 'echo "$COMPOSE_CONF_LIST"')
        assert split_and_strip(get_command_stdout(proc)) == [f"-f {tmp_build_dir}/docker-compose.yml"]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_compose_no_overrides(self, read_config_include_file, tmp_build_dir):
        """Test that COMPOSE_CONF_LIST is set correctly when there are no overrides"""
        proc = self.run_func(
            read_config_include_file,
            {"ALL_CONF_DIRS": "./config/finch ./config/raven", "BUILD_DIR": tmp_build_dir},
            'echo "$COMPOSE_CONF_LIST"'
        )
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == [
            f"{tmp_build_dir}/docker-compose.yml",
            f"{tmp_build_dir}/finch/docker-compose-extra.yml",
            f"{tmp_build_dir}/raven/docker-compose-extra.yml",
        ]

    def test_compose_in_order(self, read_config_include_file):
        """Test that the order of ALL_CONF_DIRS is respected"""
        proc1 = self.run_func(
            read_config_include_file, {"ALL_CONF_DIRS": "./config/finch ./config/raven"}, 'echo "$COMPOSE_CONF_LIST"'
        )
        out1 = split_and_strip(get_command_stdout(proc1), split_on="-f")
        proc2 = self.run_func(
            read_config_include_file, {"ALL_CONF_DIRS": "./config/raven ./config/finch"}, 'echo "$COMPOSE_CONF_LIST"'
        )
        out2 = split_and_strip(get_command_stdout(proc2), split_on="-f")
        assert out1 == out2[:1] + out2[:0:-1]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_compose_overrides(self, read_config_include_file, tmp_build_dir):
        """Test that COMPOSE_CONF_LIST is set correctly when there are overrides"""
        proc = self.run_func(
            read_config_include_file,
            {"ALL_CONF_DIRS": "./config/finch ./config/magpie", "BUILD_DIR": tmp_build_dir},
            'echo "$COMPOSE_CONF_LIST"'
        )
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == [
            f"{tmp_build_dir}/docker-compose.yml",
            f"{tmp_build_dir}/finch/docker-compose-extra.yml",
            f"{tmp_build_dir}/magpie/docker-compose-extra.yml",
            f"{tmp_build_dir}/finch/config/magpie/docker-compose-extra.yml",
        ]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_default_all_conf_dirs(self, read_config_include_file, tmp_build_dir):
        proc = self.run_func(
            read_config_include_file,
            {"ALL_CONF_DIRS": " ".join(TestReadConfigs.default_all_conf_order), "BUILD_DIR": tmp_build_dir},
            'echo "$COMPOSE_CONF_LIST"',
        )
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == self.default_conf_list_order(tmp_build_dir)
