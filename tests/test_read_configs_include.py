import io
import os
import re
import tempfile
import pytest
import subprocess
from typing import Optional, Union

ENV_SPLIT_STR: str = "#env for testing#"
ENV_SPLIT_STR_ALT: str = "#env for testing alt#"

# Set backwards compatible allowed to False explicitly since the current default
# is True when not executing through the CLI.
DEFAULT_BIRDHOUSE_ENV = {"BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False"}

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


def set_local_env(env_file: io.FileIO, content: Union[str, dict]) -> None:
    env_file.truncate()
    if isinstance(content, dict):
        content = {**DEFAULT_BIRDHOUSE_ENV, **content}
        env_file.write("\n".join(f"export {k}={v}" for k, v in content.items()))
    else:
        default_content = "\n".join([f"{k}={v}" for k, v in DEFAULT_BIRDHOUSE_ENV.items()])
        env_file.write(f"{default_content}\n{content}")


def split_and_strip(s: str, split_on="\n") -> list[str]:
    return [cline for line in s.split(split_on) if (cline := line.strip())]


def get_read_config_stdout(proc: subprocess.CompletedProcess) -> str:
    return proc.stdout.split(ENV_SPLIT_STR)[0]


def get_command_stdout(proc: subprocess.CompletedProcess) -> str:
    return proc.stdout.split(ENV_SPLIT_STR)[1]


class _ReadConfigsMixin:
    test_func: str

    def run_func(
            self, include_file: str,
            local_env: Optional[dict] = None,
            local_env_file_content: Union[str, dict] = "",
            command_suffix: str = "",
            test_func: Optional[str] = None,
    ) -> subprocess.CompletedProcess:
        if test_func is None:
            test_func = self.test_func
        try:
            env = {**DEFAULT_BIRDHOUSE_ENV, **(local_env or {})}
            if local_env_file_content:
                with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
                    set_local_env(f, local_env_file_content)

                env["BIRDHOUSE_LOCAL_ENV"] = f.name

            if command_suffix:
                command_suffix = f"&& echo '{ENV_SPLIT_STR}' && {command_suffix}"
            command = f". {include_file} && {test_func} {command_suffix}"
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
            print(proc.stdout)  # useful for debugging when test fails
            return proc
        finally:
            if local_env_file_content:
                os.unlink(f.name)


class TestReadConfigs(_ReadConfigsMixin):
    test_func = "read_configs"

    default_all_conf_order: list[str] = [
        "./components/proxy",
        "./components/magpie",
        "./components/twitcher",
        "./components/cowbird",
        "./components/stac",
    ]

    default_all_conf_order_with_dependencies: list[str] = [
        "./components/proxy",
        "./components/magpie",
        "./components/twitcher",
        "./components/wps_outputs-volume",
        "./components/cowbird",
        "./components/stac",
    ]

    extra_conf_order: list[str] = [
        "./components/canarie-api",
        "./components/geoserver",
        "./components/wps_outputs-volume",
        "./components/postgres",
        "./components/finch",
        "./components/raven",
        "./components/data-volume",
        "./components/hummingbird",
        "./components/thredds",
        "./components/jupyterhub"
    ]

    def test_return_code(self, read_config_include_file) -> None:
        """Test that the return code is 0"""
        proc = self.run_func(read_config_include_file, local_env_file_content={})
        assert proc.returncode == 0

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_all_conf_dirs_set(self, read_config_include_file) -> None:
        """Test that the ALL_CONF_DIRS variable is set"""
        proc = self.run_func(read_config_include_file, command_suffix='echo "$ALL_CONF_DIRS"')
        assert get_command_stdout(proc).strip()

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_all_conf_dirs_default_order(self, read_config_include_file) -> None:
        """Test that the expected order that default.env files are loaded is correct"""
        proc = self.run_func(read_config_include_file,
                             command_suffix='echo "$ALL_CONF_DIRS"')
        conf_dirs = self.default_all_conf_order_with_dependencies
        assert split_and_strip(get_command_stdout(proc))[:len(conf_dirs)] == conf_dirs

    def test_all_conf_dirs_extra_last(self, read_config_include_file) -> None:
        """Test that any extra components are loaded last"""
        extra = {"BIRDHOUSE_EXTRA_CONF_DIRS": '"./components/finch\n./components/weaver"'}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "$ALL_CONF_DIRS"')
        assert split_and_strip(get_command_stdout(proc))[-2:] == [
            "./components/finch",
            "./components/weaver",
        ]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_dependencies_loaded_first(self, read_config_include_file) -> None:
        """Test that dependencies are loaded first"""
        extra = {"BIRDHOUSE_EXTRA_CONF_DIRS": '"./optional-components/test-weaver"'}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "$ALL_CONF_DIRS"')
        assert split_and_strip(get_command_stdout(proc))[-2:] == [
            "./components/weaver",
            "./optional-components/test-weaver",
        ]

    def test_non_project_components_included(self, read_config_include_file) -> None:
        """Test that extra components can be included"""
        extra = {"BIRDHOUSE_EXTRA_CONF_DIRS": '"./blah/other-random-component"'}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "$ALL_CONF_DIRS"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "./blah/other-random-component"

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_delayed_eval_default_value(self, read_config_include_file) -> None:
        """Test delayed eval when value not set in env.local"""
        extra = {"BIRDHOUSE_FQDN": '"fqdn.example.com"',
                 "BIRDHOUSE_EXTRA_CONF_DIRS": '"./components/jupyterhub ./components/geoserver"'}
        command_suffix = 'echo "$BIRDHOUSE_FQDN_PUBLIC - $JUPYTERHUB_USER_DATA_DIR - $GEOSERVER_DATA_DIR"'
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix=command_suffix)
        # By default, BIRDHOUSE_FQDN_PUBLIC has same value as BIRDHOUSE_FQDN.
        assert (split_and_strip(get_command_stdout(proc))[-1] ==
                "fqdn.example.com - /data/jupyterhub_user_data - /data/geoserver")

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_delayed_eval_custom_value(self, read_config_include_file) -> None:
        """Test delayed eval when value is set in env.local"""
        extra = {"BIRDHOUSE_FQDN": '"fqdn.example.com"',
                 "BIRDHOUSE_FQDN_PUBLIC": '"public.example.com"',
                 "BIRDHOUSE_EXTRA_CONF_DIRS": '"./components/jupyterhub ./components/geoserver"',
                 "BIRDHOUSE_DATA_PERSIST_ROOT": '"/my-data-root"',  # indirectly change JUPYTERHUB_USER_DATA_DIR
                 "GEOSERVER_DATA_DIR": '"/my-geoserver-data"',
                 }
        command_suffix = 'echo "$BIRDHOUSE_FQDN_PUBLIC - $JUPYTERHUB_USER_DATA_DIR - $GEOSERVER_DATA_DIR"'
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix=command_suffix)
        # If BIRDHOUSE_FQDN_PUBLIC is set in env.local, that value should be effective.
        assert (split_and_strip(get_command_stdout(proc))[-1] ==
                "public.example.com - /my-data-root/jupyterhub_user_data - /my-geoserver-data")

    def test_delayed_eval_quoting(self, read_config_include_file) -> None:
        """Test that the delayed evaluation functions resolve quotation marks and braces properly"""
        extra = {"EXTRA_TEST_VAR": "\"{'123'}\"", "DELAYED_EVAL": "$DELAYED_EVAL EXTRA_TEST_VAR"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${EXTRA_TEST_VAR}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "{'123'}"


class TestBackwardsCompatible(_ReadConfigsMixin):
    test_func = "read_configs"

    # copy of BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES from birdhouse/default.env
    all_overrides = """
        PAVICS_FQDN=BIRDHOUSE_FQDN
        PAVICS_FQDN_PUBLIC=BIRDHOUSE_FQDN_PUBLIC
        POSTGRES_PAVICS_USERNAME=BIRDHOUSE_POSTGRES_USERNAME
        POSTGRES_PAVICS_PASSWORD=BIRDHOUSE_POSTGRES_PASSWORD
        OWNER_PAVICS_CHECKOUT=BIRDHOUSE_REPO_CHECKOUT_OWNER
        PAVICS_LOG_DIR=BIRDHOUSE_LOG_DIR
        PAVICS_FRONTEND_IP=BIRDHOUSE_FRONTEND_IP
        PAVICS_FRONTEND_PORT=BIRDHOUSE_FRONTEND_PORT
        PAVICS_FRONTEND_PROTO=BIRDHOUSE_FRONTEND_PROTO
        PAVICS_HOST_URL=BIRDHOUSE_HOST_URL
        DATA_PERSIST_ROOT=BIRDHOUSE_DATA_PERSIST_ROOT
        DATA_PERSIST_SHARED_ROOT=BIRDHOUSE_DATA_PERSIST_SHARED_ROOT
        SSL_CERTIFICATE=BIRDHOUSE_SSL_CERTIFICATE
        DOC_URL=BIRDHOUSE_DOC_URL
        SUPPORT_EMAIL=BIRDHOUSE_SUPPORT_EMAIL
        EXTRA_CONF_DIRS=BIRDHOUSE_EXTRA_CONF_DIRS
        DEFAULT_CONF_DIRS=BIRDHOUSE_DEFAULT_CONF_DIRS
        AUTODEPLOY_EXTRA_REPOS=BIRDHOUSE_AUTODEPLOY_EXTRA_REPOS
        AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=BIRDHOUSE_AUTODEPLOY_DEPLOY_KEY_ROOT_DIR
        AUTODEPLOY_PLATFORM_FREQUENCY=BIRDHOUSE_AUTODEPLOY_PLATFORM_FREQUENCY
        AUTODEPLOY_NOTEBOOK_FREQUENCY=BIRDHOUSE_AUTODEPLOY_NOTEBOOK_FREQUENCY
        AUTODEPLOY_EXTRA_SCHEDULER_JOBS=BIRDHOUSE_AUTODEPLOY_EXTRA_SCHEDULER_JOBS
        LOGROTATE_DATA_DIR=BIRDHOUSE_LOGROTATE_DATA_DIR
        ALLOW_UNSECURE_HTTP=BIRDHOUSE_ALLOW_UNSECURE_HTTP
        DOCKER_NOTEBOOK_IMAGES=JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES
        ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS=JUPYTERHUB_ENABLE_MULTI_NOTEBOOKS
        MOUNT_IMAGE_SPECIFIC_NOTEBOOKS=JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS
        EXTRA_PYWPS_CONFIG=BIRDHOUSE_EXTRA_PYWPS_CONFIG
        GITHUB_CLIENT_ID=MAGPIE_GITHUB_CLIENT_ID
        GITHUB_CLIENT_SECRET=MAGPIE_GITHUB_CLIENT_SECRET
        VERIFY_SSL=BIRDHOUSE_VERIFY_SSL
        SMTP_SERVER=ALERTMANAGER_SMTP_SERVER
        COMPOSE_UP_EXTRA_OPTS=BIRDHOUSE_COMPOSE_UP_EXTRA_OPTS
        WPS_OUTPUTS_DIR=BIRDHOUSE_WPS_OUTPUTS_DIR
        SERVER_DOC_URL=BIRDHOUSE_DOC_URL
        SERVER_SUPPORT_EMAIL=BIRDHOUSE_SUPPORT_EMAIL
        SERVER_SSL_CERTIFICATE=BIRDHOUSE_SSL_CERTIFICATE
        SERVER_DATA_PERSIST_SHARED_ROOT=BIRDHOUSE_DATA_PERSIST_SHARED_ROOT
        SERVER_WPS_OUTPUTS_DIR=BIRDHOUSE_WPS_OUTPUTS_DIR
        SERVER_NAME=BIRDHOUSE_NAME
        SERVER_DESCRIPTION=BIRDHOUSE_DESCRIPTION
        SERVER_INSTITUTION=BIRDHOUSE_INSTITUTION
        SERVER_SUBJECT=BIRDHOUSE_SUBJECT
        SERVER_TAGS=BIRDHOUSE_TAGS
        SERVER_DOCUMENTATION_URL=BIRDHOUSE_DOCUMENTATION_URL
        SERVER_RELEASE_NOTES_URL=BIRDHOUSE_RELEASE_NOTES_URL
        SERVER_SUPPORT_URL=BIRDHOUSE_SUPPORT_URL
        SERVER_LICENSE_URL=BIRDHOUSE_LICENSE_URL
    """

    old_vars = {line.strip().split("=")[0]: "old" for line in all_overrides.splitlines() if line.strip()}
    new_vars = {line.strip().split("=")[1]: "new" for line in all_overrides.splitlines() if line.strip()}

    def test_allowed_simple_substitution(self, read_config_include_file) -> None:
        """
        Test that a deprecated variable can be used to set the new version if backwards compatible
        variables are allowed.
        """
        extra = {"PAVICS_FQDN": "fqdn.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${BIRDHOUSE_FQDN}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "fqdn.example.com"

    def test_not_allowed_simple_substitution(self, read_config_include_file):
        """
        Test that a deprecated variable cannot be used to set the new version if backwards compatible
        variables are not allowed.
        """
        extra = {"PAVICS_FQDN": "fqdn.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${BIRDHOUSE_FQDN}"')
        assert not split_and_strip(get_command_stdout(proc))

    def test_allowed_simple_override(self, read_config_include_file) -> None:
        """
        Test that a deprecated variable can be used to override the new version if backwards compatible
        variables are allowed.
        """
        extra = {"PAVICS_FQDN": "pavics.example.com",
                 "BIRDHOUSE_FQDN": "birdhouse.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${BIRDHOUSE_FQDN}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "pavics.example.com"

    def test_not_allowed_simple_override(self, read_config_include_file):
        """
        Test that a deprecated variable cannot be used to override the new version if backwards compatible
        variables are not allowed.
        """
        extra = {"PAVICS_FQDN": "pavics.example.com",
                 "BIRDHOUSE_FQDN": "birdhouse.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${BIRDHOUSE_FQDN}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "birdhouse.example.com"

    def test_allowed_substitution_all(self, read_config_include_file):
        """
        Test that all deprecated variables can be used to set the new versions if backwards compatible
        variables are allowed.
        """
        command_suffix = f'echo "{ENV_SPLIT_STR_ALT.join(f"{k}=${k}" for k in self.new_vars)}"'
        proc = self.run_func(read_config_include_file,
                             local_env_file_content={"BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True", **self.old_vars},
                             command_suffix=command_suffix)
        expected = set()
        for k in self.new_vars:
            if k == "BIRDHOUSE_EXTRA_CONF_DIRS":
                expected.add(f"{k}=old ./optional-components/backwards-compatible-overrides")
            else:
                expected.add(f"{k}=old")
        assert {re.sub(r'[\s\n]+', ' ', val.strip()) for val in
                get_command_stdout(proc).split(ENV_SPLIT_STR_ALT)} == expected

    def test_not_allowed_substitution_all(self, read_config_include_file):
        """
        Test that all deprecated variables are not used to set the new versions if backwards compatible
        variables are not allowed.
        """
        command_suffix = f'echo "{ENV_SPLIT_STR_ALT.join(f"{k}=${k}" for k in self.new_vars)}"'
        proc = self.run_func(read_config_include_file,
                             local_env_file_content={"BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False", **self.old_vars},
                             command_suffix=command_suffix)
        expected = set()
        for k in self.new_vars:
            expected.add(f"{k}=new")
        actual = [re.sub(r'[\s\n]+', ' ', val.strip()) for val in get_command_stdout(proc).split(ENV_SPLIT_STR_ALT)]
        assert all(val != "new" for val in actual)

    def test_allowed_override_all(self, read_config_include_file):
        """
        Test that all deprecated variables can be used to override the new versions if backwards compatible
        variables are allowed.
        """
        command_suffix = f'echo "{ENV_SPLIT_STR_ALT.join(f"{k}=${k}" for k in self.new_vars)}"'
        proc = self.run_func(read_config_include_file,
                             local_env_file_content={"BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True", **self.old_vars,
                                                     **self.new_vars},
                             command_suffix=command_suffix)
        expected = set()
        for k in self.new_vars:
            if k == "BIRDHOUSE_EXTRA_CONF_DIRS":
                expected.add(f"{k}=old ./optional-components/backwards-compatible-overrides")
            else:
                expected.add(f"{k}=old")
        assert {re.sub(r'[\s\n]+', ' ', val.strip()) for val in
                get_command_stdout(proc).split(ENV_SPLIT_STR_ALT)} == expected

    def test_not_allowed_override_all(self, read_config_include_file):
        """
        Test that all deprecated variables are not used to override the new versions if backwards compatible
        variables are not allowed.
        """
        command_suffix = f'echo "{ENV_SPLIT_STR_ALT.join(f"{k}=${k}" for k in self.new_vars)}"'
        proc = self.run_func(read_config_include_file,
                             local_env_file_content={"BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False", **self.old_vars,
                                                     **self.new_vars},
                             command_suffix=command_suffix)
        assert {re.sub(r'[\s\n]+', ' ', val.strip()) for val in
                get_command_stdout(proc).split(ENV_SPLIT_STR_ALT)} == {f"{k}=new" for k in self.new_vars}

    def test_allowed_set_old_variables_when_unset(self, read_config_include_file):
        """
        Test that new variables can be used to set deprecated variables when the deprecated variable is unset if
        backwards compatible variables are allowed.
        """
        extra = {"BIRDHOUSE_FQDN": "birdhouse.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${PAVICS_FQDN}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "birdhouse.example.com"

    def test_not_allowed_set_old_variables_when_unset(self, read_config_include_file):
        """
        Test that new variables cannot be used to set deprecated variables when the deprecated variable is unset if
        backwards compatible variables are not allowed.
        """
        extra = {"BIRDHOUSE_FQDN": "birdhouse.example.com", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${PAVICS_FQDN}"')
        assert not split_and_strip(get_command_stdout(proc))

    def test_allowed_no_override_old_variables_when_set(self, read_config_include_file):
        """
        Test that new variables cannot be used to override deprecated variables when the deprecated variable is set if
        backwards compatible variables are allowed.
        """
        extra = {"PAVICS_FQDN": "pavics.example.com", "BIRDHOUSE_FQDN": "birdhouse.example.com",
                 "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "True"}
        proc = self.run_func(read_config_include_file, local_env_file_content=extra,
                             command_suffix='echo "${PAVICS_FQDN}"')
        assert split_and_strip(get_command_stdout(proc))[-1] == "pavics.example.com"


class TestCreateComposeConfList(_ReadConfigsMixin):
    test_func = "create_compose_conf_list"

    default_conf_list_order: list[str] = [
        "docker-compose.yml",
        "./components/proxy/docker-compose-extra.yml",
        "./components/magpie/docker-compose-extra.yml",
        "./components/magpie/config/proxy/docker-compose-extra.yml",
        "./components/twitcher/docker-compose-extra.yml",
        "./components/twitcher/config/proxy/docker-compose-extra.yml",
        "./components/cowbird/docker-compose-extra.yml",
        "./components/cowbird/config/magpie/docker-compose-extra.yml",
        "./components/cowbird/config/proxy/docker-compose-extra.yml",
        "./components/stac/docker-compose-extra.yml",
        "./components/stac/config/magpie/docker-compose-extra.yml",
        "./components/stac/config/proxy/docker-compose-extra.yml",
        "./components/stac/config/twitcher/docker-compose-extra.yml",
        "./components/canarie-api/docker-compose-extra.yml",
        "./components/magpie/config/canarie-api/docker-compose-extra.yml",
        "./components/twitcher/config/canarie-api/docker-compose-extra.yml",
        "./components/cowbird/config/canarie-api/docker-compose-extra.yml",
        "./components/stac/config/canarie-api/docker-compose-extra.yml",
        "./components/canarie-api/config/proxy/docker-compose-extra.yml",
        "./components/geoserver/docker-compose-extra.yml",
        "./components/cowbird/config/geoserver/docker-compose-extra.yml",
        "./components/geoserver/config/canarie-api/docker-compose-extra.yml",
        "./components/geoserver/config/magpie/docker-compose-extra.yml",
        "./components/geoserver/config/proxy/docker-compose-extra.yml",
        "./components/wps_outputs-volume/docker-compose-extra.yml",
        "./components/wps_outputs-volume/config/canarie-api/docker-compose-extra.yml",
        "./components/wps_outputs-volume/config/proxy/docker-compose-extra.yml",
        "./components/postgres/docker-compose-extra.yml",
        "./components/finch/docker-compose-extra.yml",
        "./components/finch/config/canarie-api/docker-compose-extra.yml",
        "./components/finch/config/magpie/docker-compose-extra.yml",
        "./components/finch/config/wps_outputs-volume/docker-compose-extra.yml",
        "./components/raven/docker-compose-extra.yml",
        "./components/raven/config/canarie-api/docker-compose-extra.yml",
        "./components/raven/config/magpie/docker-compose-extra.yml",
        "./components/raven/config/wps_outputs-volume/docker-compose-extra.yml",
        "./components/data-volume/docker-compose-extra.yml",
        "./components/hummingbird/docker-compose-extra.yml",
        "./components/hummingbird/config/canarie-api/docker-compose-extra.yml",
        "./components/hummingbird/config/data-volume/docker-compose-extra.yml",
        "./components/hummingbird/config/magpie/docker-compose-extra.yml",
        "./components/hummingbird/config/wps_outputs-volume/docker-compose-extra.yml",
        "./components/thredds/docker-compose-extra.yml",
        "./components/thredds/config/canarie-api/docker-compose-extra.yml",
        "./components/thredds/config/magpie/docker-compose-extra.yml",
        "./components/thredds/config/proxy/docker-compose-extra.yml",
        "./components/jupyterhub/docker-compose-extra.yml",
        "./components/cowbird/config/jupyterhub/docker-compose-extra.yml",
        "./components/jupyterhub/config/canarie-api/docker-compose-extra.yml",
        "./components/jupyterhub/config/magpie/docker-compose-extra.yml",
        "./components/jupyterhub/config/proxy/docker-compose-extra.yml"
    ]

    def test_all_conf_dirs_empty(self, read_config_include_file):
        """Test that only the base compose file is used when ALL_CONF_DIRS is empty"""
        proc = self.run_func(read_config_include_file, command_suffix='echo "$COMPOSE_CONF_LIST"')
        assert split_and_strip(get_command_stdout(proc)) == ["-f docker-compose.yml"]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_compose_no_overrides(self, read_config_include_file):
        """Test that COMPOSE_CONF_LIST is set correctly when there are no overrides"""
        proc = self.run_func(
            read_config_include_file, local_env={"ALL_CONF_DIRS": "./components/finch ./components/raven"},
            command_suffix='echo "$COMPOSE_CONF_LIST"'
        )
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == [
            "docker-compose.yml",
            "./components/finch/docker-compose-extra.yml",
            "./components/raven/docker-compose-extra.yml",
        ]

    def test_compose_in_order(self, read_config_include_file):
        """Test that the order of ALL_CONF_DIRS is respected"""
        proc1 = self.run_func(
            read_config_include_file, local_env={"ALL_CONF_DIRS": "./components/finch ./components/raven"},
            command_suffix='echo "$COMPOSE_CONF_LIST"'
        )
        out1 = split_and_strip(get_command_stdout(proc1), split_on="-f")
        proc2 = self.run_func(
            read_config_include_file, local_env={"ALL_CONF_DIRS": "./components/raven ./components/finch"},
            command_suffix='echo "$COMPOSE_CONF_LIST"'
        )
        out2 = split_and_strip(get_command_stdout(proc2), split_on="-f")
        assert out1 == out2[:1] + out2[:0:-1]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_compose_overrides(self, read_config_include_file):
        """Test that COMPOSE_CONF_LIST is set correctly when there are overrides"""
        proc = self.run_func(
            read_config_include_file, local_env={"ALL_CONF_DIRS": "./components/finch ./components/magpie"},
            command_suffix='echo "$COMPOSE_CONF_LIST"'
        )
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == [
            "docker-compose.yml",
            "./components/finch/docker-compose-extra.yml",
            "./components/magpie/docker-compose-extra.yml",
            "./components/finch/config/magpie/docker-compose-extra.yml",
        ]

    @pytest.mark.usefixtures("run_in_compose_dir")
    def test_default_all_conf_dirs(self, read_config_include_file):
        proc = self.run_func(
            read_config_include_file,
            local_env={
                "ALL_CONF_DIRS": " ".join(TestReadConfigs.default_all_conf_order + TestReadConfigs.extra_conf_order)},
            command_suffix='echo "$COMPOSE_CONF_LIST"',
        )
        print(proc.stdout)  # useful for debugging when assert fail
        assert split_and_strip(get_command_stdout(proc), split_on="-f") == self.default_conf_list_order
