import asyncio
from http.cookies import Morsel
import importlib
import json
import os
import sys
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from importlib import reload

import pytest
import requests.cookies
import yaml


@pytest.fixture(scope="module")
def jupyterhub_custom_initial_load(root_dir):
    path = root_dir / "birdhouse" / "components" / "jupyterhub" / "jupyterhub_custom"
    sys.path.append(str(path))
    return importlib.import_module("jupyterhub_custom")


@pytest.fixture(autouse=True)
def jupyterhub_custom(jupyterhub_custom_initial_load):
    return reload(jupyterhub_custom_initial_load)


TEST_ENV = {
    "JUPYTERHUB_USER_DATA_DIR": "user-data",
    "WORKSPACE_DIR": "workspace",
    "JUPYTER_GOOGLE_DRIVE_SETTINGS": "drive-settings",
    "JUPYTERHUB_RESOURCE_LIMITS": "",
    "JUPYTERHUB_README": "test-readme",
    "JUPYTER_IDLE_SERVER_CULL_TIMEOUT": "1",
    "JUPYTER_IDLE_KERNEL_CULL_TIMEOUT": "2",
    "JUPYTER_IDLE_KERNEL_CULL_INTERVAL": "3",
    "BIRDHOUSE_FQDN_PUBLIC": "example.com",
    "JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL": "http://example.com/test/auth",
    "JUPYTERHUB_CRYPT_KEY": "test-key",
    "JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE": "4",
    "JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES": "test1 test2",
    "JUPYTERHUB_IMAGE_SELECTION_NAMES": "image1 image2",
    "JUPYTERHUB_ALLOWED_IMAGES": '{"a": "test1", "b": "test2", "c": "test3"}',
    "DOCKER_NETWORK_NAME": "test-network",
    "BIRDHOUSE_PROXY_SCHEME": "http",
    "PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR": "wps-output",
    "JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS": "true",
    "USER_WORKSPACE_UID": "1001",
    "USER_WORKSPACE_GID": "1002",
    "JUPYTER_DEMO_USER": "demo-user",
    "JUPYTER_DEMO_USER_CPU_LIMIT": "1.2",
    "JUPYTER_DEMO_USER_MEM_LIMIT": "3M",
    "JUPYTERHUB_ADMIN_GROUP_NAME": "admin-group",
    "JUPYTERHUB_DOCKER_EXTRA_HOSTS": "hostname:network other:other-network",
}

BACK_COMPAT_VARS = [
    "notebook_dir",
    "jupyterhub_data_dir",
    "container_workspace_dir",
    "container_home_dir",
    "user_kernels_dir",
    "host_user_data_dir",
    "container_gdrive_settings_path",
    "host_gdrive_settings_path",
    "resource_limits",
    "readme",
    "jupyter_idle_server_cull_timeout",
    "jupyter_idle_kernel_cull_timeout",
    "jupyter_idle_kernel_cull_interval",
]


@pytest.fixture
def mock_env(monkeypatch):
    with patch.dict(os.environ, clear=True):
        for key, val in TEST_ENV.items():
            monkeypatch.setenv(key, val)
        yield


@pytest.fixture
def constants(mock_env):
    yield reload(importlib.import_module("jupyterhub_custom.constants"))


class TestConstants:
    def check_required(self, env_var, constants, monkeypatch):
        monkeypatch.delenv(env_var)
        with pytest.raises(KeyError):
            reload(constants)

    def test_JUPYTERHUB_DATA_DIR(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_DATA_DIR == TEST_ENV["JUPYTERHUB_USER_DATA_DIR"]
        self.check_required("JUPYTERHUB_USER_DATA_DIR", constants, monkeypatch)

    def test_WORKSPACE_DIR(self, constants, monkeypatch):
        assert constants.WORKSPACE_DIR == TEST_ENV["WORKSPACE_DIR"]
        self.check_required("WORKSPACE_DIR", constants, monkeypatch)

    def test_HOST_USER_DATA_DIR(self, constants):
        assert constants.HOST_USER_DATA_DIR == os.path.join(TEST_ENV["WORKSPACE_DIR"], "{username}")

    def test_HOST_GDRIVE_SETTINGS_PATH(self, constants, monkeypatch):
        assert constants.HOST_GDRIVE_SETTINGS_PATH == TEST_ENV["JUPYTER_GOOGLE_DRIVE_SETTINGS"]
        self.check_required("JUPYTER_GOOGLE_DRIVE_SETTINGS", constants, monkeypatch)

    def test_RESOURCE_LIMITS(self, constants, monkeypatch):
        assert constants.RESOURCE_LIMITS == []
        json_val = [{"a": "b"}]
        yaml_val = [{"c": "d"}]
        monkeypatch.setenv("JUPYTERHUB_RESOURCE_LIMITS", json.dumps(json_val))
        assert reload(constants).RESOURCE_LIMITS == json_val
        monkeypatch.setenv("JUPYTERHUB_RESOURCE_LIMITS", yaml.dump(yaml_val))
        assert reload(constants).RESOURCE_LIMITS == yaml_val
        monkeypatch.delenv("JUPYTERHUB_RESOURCE_LIMITS")
        assert reload(constants).RESOURCE_LIMITS == []

    def test_README(self, constants, monkeypatch):
        assert constants.README == TEST_ENV["JUPYTERHUB_README"]
        monkeypatch.delenv("JUPYTERHUB_README")
        assert reload(constants).README == ""

    def test_JUPYTER_IDLE_SERVER_CULL_TIMEOUT(self, constants, monkeypatch):
        assert constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT == int(TEST_ENV["JUPYTER_IDLE_SERVER_CULL_TIMEOUT"])
        monkeypatch.delenv("JUPYTER_IDLE_SERVER_CULL_TIMEOUT")
        assert reload(constants).JUPYTER_IDLE_SERVER_CULL_TIMEOUT == 0

    def test_JUPYTER_IDLE_KERNEL_CULL_TIMEOUT(self, constants, monkeypatch):
        assert constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT == int(TEST_ENV["JUPYTER_IDLE_KERNEL_CULL_TIMEOUT"])
        monkeypatch.delenv("JUPYTER_IDLE_KERNEL_CULL_TIMEOUT")
        assert reload(constants).JUPYTER_IDLE_KERNEL_CULL_TIMEOUT == 0

    def test_JUPYTER_IDLE_KERNEL_CULL_INTERVAL(self, constants, monkeypatch):
        assert constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL == int(TEST_ENV["JUPYTER_IDLE_KERNEL_CULL_INTERVAL"])
        monkeypatch.delenv("JUPYTER_IDLE_KERNEL_CULL_INTERVAL")
        assert reload(constants).JUPYTER_IDLE_KERNEL_CULL_INTERVAL == 0

    def test_BIRDHOUSE_FQDN_PUBLIC(self, constants, monkeypatch):
        assert constants.BIRDHOUSE_FQDN_PUBLIC == TEST_ENV["BIRDHOUSE_FQDN_PUBLIC"]
        self.check_required("BIRDHOUSE_FQDN_PUBLIC", constants, monkeypatch)

    def test_JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL(self, constants, monkeypatch):
        assert (
            constants.JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL
            == TEST_ENV["JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL"]
        )
        monkeypatch.delenv("JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL")
        assert reload(constants).JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL == ""

    def test_JUPYTERHUB_CRYPT_KEY_IS_SET(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_CRYPT_KEY_IS_SET == bool(TEST_ENV["JUPYTERHUB_CRYPT_KEY"])
        monkeypatch.delenv("JUPYTERHUB_CRYPT_KEY")
        assert not reload(constants).JUPYTERHUB_CRYPT_KEY_IS_SET

    def test_JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE == int(TEST_ENV["JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE"])
        monkeypatch.delenv("JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE")
        assert reload(constants).JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE == 0

    def test_JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES == TEST_ENV["JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES"].split()
        self.check_required("JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES", constants, monkeypatch)

    def test_JUPYTERHUB_IMAGE_SELECTION_NAMES(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_IMAGE_SELECTION_NAMES == TEST_ENV["JUPYTERHUB_IMAGE_SELECTION_NAMES"].split()
        self.check_required("JUPYTERHUB_IMAGE_SELECTION_NAMES", constants, monkeypatch)

    def test_JUPYTERHUB_ALLOWED_IMAGES(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_ALLOWED_IMAGES == yaml.safe_load(TEST_ENV["JUPYTERHUB_ALLOWED_IMAGES"])
        json_val = {"a": "b"}
        yaml_val = {"c": "d"}
        monkeypatch.setenv("JUPYTERHUB_ALLOWED_IMAGES", json.dumps(json_val))
        assert reload(constants).JUPYTERHUB_ALLOWED_IMAGES == json_val
        monkeypatch.setenv("JUPYTERHUB_ALLOWED_IMAGES", yaml.dump(yaml_val))
        assert reload(constants).JUPYTERHUB_ALLOWED_IMAGES == yaml_val
        monkeypatch.delenv("JUPYTERHUB_ALLOWED_IMAGES")
        assert reload(constants).JUPYTERHUB_ALLOWED_IMAGES is None

    def test_DOCKER_NETWORK_NAME(self, constants, monkeypatch):
        assert constants.DOCKER_NETWORK_NAME == TEST_ENV["DOCKER_NETWORK_NAME"]
        self.check_required("DOCKER_NETWORK_NAME", constants, monkeypatch)

    def test_BIRDHOUSE_HOST_URL(self, constants, monkeypatch):
        assert (
            constants.BIRDHOUSE_HOST_URL
            == f"{TEST_ENV['BIRDHOUSE_PROXY_SCHEME']}://{TEST_ENV['BIRDHOUSE_FQDN_PUBLIC']}"
        )
        self.check_required("BIRDHOUSE_PROXY_SCHEME", constants, monkeypatch)

    def test_PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR(self, constants, monkeypatch):
        assert constants.PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR == TEST_ENV["PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR"]
        monkeypatch.delenv("PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR")
        assert reload(constants).PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR == ""

    def test_COWBIRD_ENABLED(self, constants, monkeypatch):
        monkeypatch.setenv("WORKSPACE_DIR", "test1")
        monkeypatch.setenv("JUPYTERHUB_USER_DATA_DIR", "test1")
        assert not reload(constants).COWBIRD_ENABLED
        monkeypatch.setenv("JUPYTERHUB_USER_DATA_DIR", "test2")
        assert reload(constants).COWBIRD_ENABLED

    def test_JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS
        monkeypatch.setenv("JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS", "somethingelse")
        assert not reload(constants).JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS
        monkeypatch.delenv("JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS")
        assert not reload(constants).JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS

    def test_USER_WORKSPACE_UID(self, constants, monkeypatch):
        assert constants.USER_WORKSPACE_UID == TEST_ENV["USER_WORKSPACE_UID"]
        self.check_required("USER_WORKSPACE_UID", constants, monkeypatch)

    def test_USER_WORKSPACE_GID(self, constants, monkeypatch):
        assert constants.USER_WORKSPACE_GID == TEST_ENV["USER_WORKSPACE_GID"]
        self.check_required("USER_WORKSPACE_GID", constants, monkeypatch)

    def test_JUPYTER_DEMO_USER(self, constants, monkeypatch):
        assert constants.JUPYTER_DEMO_USER == TEST_ENV["JUPYTER_DEMO_USER"]
        self.check_required("JUPYTER_DEMO_USER", constants, monkeypatch)

    def test_JUPYTER_DEMO_USER_CPU_LIMIT(self, constants, monkeypatch):
        assert constants.JUPYTER_DEMO_USER_CPU_LIMIT == float(TEST_ENV["JUPYTER_DEMO_USER_CPU_LIMIT"])
        self.check_required("JUPYTER_DEMO_USER_CPU_LIMIT", constants, monkeypatch)

    def test_JUPYTER_DEMO_USER_MEM_LIMIT(self, constants, monkeypatch):
        assert constants.JUPYTER_DEMO_USER_MEM_LIMIT == TEST_ENV["JUPYTER_DEMO_USER_MEM_LIMIT"]
        self.check_required("JUPYTER_DEMO_USER_MEM_LIMIT", constants, monkeypatch)

    def test_JUPYTERHUB_ADMIN_GROUP_NAME(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_ADMIN_GROUP_NAME == TEST_ENV["JUPYTERHUB_ADMIN_GROUP_NAME"]
        self.check_required("JUPYTERHUB_ADMIN_GROUP_NAME", constants, monkeypatch)

    def test_JUPYTERHUB_DOCKER_EXTRA_HOSTS(self, constants, monkeypatch):
        assert constants.JUPYTERHUB_DOCKER_EXTRA_HOSTS == {"hostname": "network", "other": "other-network"}
        monkeypatch.delenv("JUPYTERHUB_DOCKER_EXTRA_HOSTS")
        reload(constants).JUPYTERHUB_DOCKER_EXTRA_HOSTS == {}

    def test_backwards_compatible_star_importable(self, constants):
        assert constants.__all__ == BACK_COMPAT_VARS

    def test_backwards_compatible_lowercase_versions(self, constants):
        back_compat_vars = {var.upper(): getattr(constants, var) for var in BACK_COMPAT_VARS}
        vars = {var.upper(): getattr(constants, var.upper()) for var in BACK_COMPAT_VARS}
        assert back_compat_vars == vars


class TestCustomDockerSpawner:
    @pytest.fixture
    def spawner(self, mock_env):
        yield reload(importlib.import_module("jupyterhub_custom.custom_dockerspawner"))

    def test_image(self, spawner, constants):
        assert spawner.CustomDockerSpawner().image == constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES[0]

    def test_network_name(self, spawner, constants):
        assert spawner.CustomDockerSpawner().network_name == constants.DOCKER_NETWORK_NAME

    def test_notebook_dir(self, spawner, constants):
        assert spawner.CustomDockerSpawner().notebook_dir == constants.NOTEBOOK_DIR

    class TestArgs:
        def test_no_timeouts(self, spawner, constants):
            constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT = 0
            constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT = 0
            constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL = 0
            reload(spawner)
            assert spawner.CustomDockerSpawner().args == ["--FileContentsManager.always_delete_dir=True"]

        def test_server_cull_timeout_only(self, spawner, constants):
            constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT = 10
            constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT = 0
            constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL = 0
            reload(spawner)
            assert spawner.CustomDockerSpawner().args == [
                "--FileContentsManager.always_delete_dir=True",
                "--NotebookApp.shutdown_no_activity_timeout=10",
                "--MappingKernelManager.cull_connected=True",
                "--TerminalManager.cull_connected=True",
            ]

        def test_kernel_cull_timeout_only(self, spawner, constants):
            constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT = 0
            constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT = 10
            constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL = 0
            reload(spawner)
            assert spawner.CustomDockerSpawner().args == [
                "--FileContentsManager.always_delete_dir=True",
                "--MappingKernelManager.cull_idle_timeout=10",
                "--MappingKernelManager.cull_interval=5",
                "--TerminalManager.cull_inactive_timeout=10",
                "--TerminalManager.cull_interval=5",
                "--MappingKernelManager.cull_connected=True",
                "--TerminalManager.cull_connected=True",
            ]

        def test_kernel_cull_timeout_and_interval(self, spawner, constants):
            constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT = 0
            constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT = 10
            constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL = 3
            reload(spawner)
            assert spawner.CustomDockerSpawner().args == [
                "--FileContentsManager.always_delete_dir=True",
                "--MappingKernelManager.cull_idle_timeout=10",
                "--MappingKernelManager.cull_interval=3",
                "--TerminalManager.cull_inactive_timeout=10",
                "--TerminalManager.cull_interval=3",
                "--MappingKernelManager.cull_connected=True",
                "--TerminalManager.cull_connected=True",
            ]

        def test_all_timeouts(self, spawner, constants):
            constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT = 6
            constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT = 10
            constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL = 3
            reload(spawner)
            assert spawner.CustomDockerSpawner().args == [
                "--FileContentsManager.always_delete_dir=True",
                "--NotebookApp.shutdown_no_activity_timeout=6",
                "--MappingKernelManager.cull_idle_timeout=10",
                "--MappingKernelManager.cull_interval=3",
                "--TerminalManager.cull_inactive_timeout=10",
                "--TerminalManager.cull_interval=3",
                "--MappingKernelManager.cull_connected=True",
                "--TerminalManager.cull_connected=True",
            ]

    class TestAllowedImages:
        def test_custom(self, spawner, constants):
            assert spawner.CustomDockerSpawner().allowed_images == constants.JUPYTERHUB_ALLOWED_IMAGES

        def test_custom_single(self, spawner, constants):
            constants.JUPYTERHUB_ALLOWED_IMAGES = {"a": "image1"}
            assert reload(spawner).CustomDockerSpawner().allowed_images == []

        def test_with_names(self, spawner, constants):
            constants.JUPYTERHUB_ALLOWED_IMAGES = None
            constants.JUPYTERHUB_IMAGE_SELECTION_NAMES = ["a", "b"]
            constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES = ["image1", "image2"]
            assert reload(spawner).CustomDockerSpawner().allowed_images == {"a": "image1", "b": "image2"}

        def test_with_names_single(self, spawner, constants):
            constants.JUPYTERHUB_ALLOWED_IMAGES = None
            constants.JUPYTERHUB_IMAGE_SELECTION_NAMES = ["a"]
            constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES = ["image1"]
            assert reload(spawner).CustomDockerSpawner().allowed_images == []

        def test_without_names(self, spawner, constants):
            constants.JUPYTERHUB_ALLOWED_IMAGES = None
            constants.JUPYTERHUB_IMAGE_SELECTION_NAMES = []
            constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES = ["image1", "image2"]
            assert reload(spawner).CustomDockerSpawner().allowed_images == constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES

        def test_without_names_single(self, spawner, constants):
            constants.JUPYTERHUB_ALLOWED_IMAGES = None
            constants.JUPYTERHUB_IMAGE_SELECTION_NAMES = []
            constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES = ["image1"]
            assert reload(spawner).CustomDockerSpawner().allowed_images == []

    class TestVolumes:
        def test_no_extras(self, spawner, constants):
            constants.COWBIRD_ENABLED = False
            constants.HOST_GDRIVE_SETTINGS_PATH = ""
            constants.README = ""
            assert reload(spawner).CustomDockerSpawner().volumes == {
                "workspace/{username}": "/notebook_dir/writable-workspace"
            }

        def test_cowbird_enabled(self, spawner, constants):
            constants.COWBIRD_ENABLED = True
            constants.HOST_GDRIVE_SETTINGS_PATH = ""
            constants.README = ""
            assert reload(spawner).CustomDockerSpawner().volumes == {
                "workspace/{username}": "/notebook_dir/writable-workspace",
                "user-data/{username}": {
                    "bind": "user-data/{username}",
                    "mode": "rw",
                },
                "workspace/wps-output": {
                    "bind": "/notebook_dir/wps-output",
                    "mode": "ro",
                },
            }

        def test_host_gdrive_path(self, spawner, constants):
            constants.COWBIRD_ENABLED = False
            constants.HOST_GDRIVE_SETTINGS_PATH = "some/path/gdrive/"
            constants.README = ""
            assert reload(spawner).CustomDockerSpawner().volumes == {
                "workspace/{username}": "/notebook_dir/writable-workspace",
                "some/path/gdrive/": {
                    "bind": constants.CONTAINER_GDRIVE_SETTINGS_PATH,
                    "mode": "ro",
                },
            }

        def test_readme(self, spawner, constants):
            constants.COWBIRD_ENABLED = False
            constants.HOST_GDRIVE_SETTINGS_PATH = ""
            constants.README = "readmepath"
            assert reload(spawner).CustomDockerSpawner().volumes == {
                "workspace/{username}": "/notebook_dir/writable-workspace",
                "readmepath": {"bind": os.path.join(constants.NOTEBOOK_DIR, "README.ipynb"), "mode": "ro"},
            }

    def test_escaped_name_return_name_as_is(self, spawner):
        spawner_inst = spawner.CustomDockerSpawner()
        spawner_inst.user = Mock()
        name = "name.with?other_chars"
        spawner_inst.user.name = name
        assert spawner_inst.escaped_name == name

    class TestPreSpawnHook:
        @pytest.fixture
        def generate_spawner_inst(self):
            def _(spawner, name="user"):
                spawner_inst = spawner.CustomDockerSpawner()
                spawner_inst.user = Mock()
                spawner_inst.user.name = name
                spawner_inst.user.groups = []
                spawner_inst.user_options = {"image": "image1"}
                return spawner_inst

            return _

        @pytest.fixture(autouse=True)
        def work_in_tmp_dir(self, constants, spawner, tmp_path):
            constants.JUPYTERHUB_DATA_DIR = os.path.join(tmp_path, constants.JUPYTERHUB_DATA_DIR)
            constants.WORKSPACE_DIR = os.path.join(tmp_path, constants.WORKSPACE_DIR)
            os.mkdir(constants.JUPYTERHUB_DATA_DIR)
            os.mkdir(constants.WORKSPACE_DIR)
            reload(spawner)

        class TestCreateTutorialNotebooks:
            def test_no_image_specific_tutorials(self, spawner, constants, generate_spawner_inst):
                constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS = False
                spawner_inst = generate_spawner_inst(spawner)
                initial_volumes = dict(spawner_inst.volumes)
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.volumes == {
                    **initial_volumes,
                    os.path.join(constants.JUPYTERHUB_DATA_DIR, "tutorial-notebooks"): {
                        "bind": "/notebook_dir/tutorial-notebooks",
                        "mode": "ro",
                    },
                }

            def test_image_specific_tutorials_dirs_no_exist(self, spawner, constants, generate_spawner_inst):
                constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS = True
                spawner_inst = generate_spawner_inst(spawner)
                initial_volumes = dict(spawner_inst.volumes)
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.volumes == initial_volumes

            def test_image_specific_tutorials_dirs_exist(self, spawner, constants, generate_spawner_inst):
                constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS = True
                spawner_inst = generate_spawner_inst(spawner)
                initial_volumes = dict(spawner_inst.volumes)
                tutorial_dir = os.path.join(
                    constants.JUPYTERHUB_DATA_DIR,
                    "tutorial-notebooks-specific-images",
                    spawner_inst.user_options["image"],
                )
                os.makedirs(tutorial_dir)
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.volumes == {
                    **initial_volumes,
                    tutorial_dir: {
                        "bind": "/notebook_dir/tutorial-notebooks",
                        "mode": "ro",
                    },
                }

            def test_image_specific_tutorials_dirs_exist_with_color(self, spawner, constants, generate_spawner_inst):
                constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS = True
                spawner_inst = generate_spawner_inst(spawner)
                initial_volumes = dict(spawner_inst.volumes)
                image_name = "image:v1"
                spawner_inst.user_options["image"] = image_name
                tutorial_dir = os.path.join(
                    constants.JUPYTERHUB_DATA_DIR,
                    "tutorial-notebooks-specific-images",
                    "image",
                )
                os.makedirs(tutorial_dir)
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.volumes == {
                    **initial_volumes,
                    tutorial_dir: {
                        "bind": "/notebook_dir/tutorial-notebooks",
                        "mode": "ro",
                    },
                }

        class TestCreateDir:
            def test_creates_jupyterhub_user_dir(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                spawner_inst.run_pre_spawn_hook()
                assert os.path.isdir(os.path.join(constants.JUPYTERHUB_DATA_DIR, spawner_inst.user.name))

            def test_ownership_change_jupyterhub_user_dir(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                with patch("subprocess.call") as mock:
                    spawner_inst.run_pre_spawn_hook()
                    assert mock.call_args_list[0][0][0] == [
                        "chown",
                        "-R",
                        f"{constants.USER_WORKSPACE_UID}:{constants.USER_WORKSPACE_GID}",
                        os.path.join(constants.JUPYTERHUB_DATA_DIR, spawner_inst.user.name),
                    ]

            def test_creates_workspace_symlink(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                spawner_inst.run_pre_spawn_hook()
                link_path = os.path.join(constants.WORKSPACE_DIR, spawner_inst.user.name)
                target_path = os.path.join(constants.JUPYTERHUB_DATA_DIR, spawner_inst.user.name)
                assert os.path.islink(link_path)
                assert os.path.realpath(link_path) == target_path

            def test_ownership_change_workspace_symlink(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                with patch("subprocess.call") as mock:
                    spawner_inst.run_pre_spawn_hook()
                    assert mock.call_args_list[1][0][0] == [
                        "chown",
                        f"{constants.USER_WORKSPACE_UID}:{constants.USER_WORKSPACE_GID}",
                        os.path.join(constants.WORKSPACE_DIR, spawner_inst.user.name),
                    ]

            def test_cowbird_not_enabled(self, spawner, constants, generate_spawner_inst):
                constants.WORKSPACE_DIR = constants.JUPYTERHUB_DATA_DIR
                constants.COWBIRD_ENABLED = False
                spawner_inst = generate_spawner_inst(spawner)
                link_path = os.path.join(constants.WORKSPACE_DIR, spawner_inst.user.name)
                with patch("subprocess.call") as mock:
                    spawner_inst.run_pre_spawn_hook()
                    assert not os.path.islink(link_path)
                    assert mock.call_count == 1

        class TestLimitResources:
            def test_user_is_demo(self, spawner, constants, generate_spawner_inst):
                mem_limit_mb = 4
                constants.JUPYTER_DEMO_USER_MEM_LIMIT = f"{mem_limit_mb}M"
                spawner_inst = generate_spawner_inst(spawner)
                spawner_inst.user.name = constants.JUPYTER_DEMO_USER
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.cpu_limit == constants.JUPYTER_DEMO_USER_CPU_LIMIT
                assert spawner_inst.mem_limit == mem_limit_mb * 1024**2

            def test_user_name_matches_cpu_limit(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                constants.RESOURCE_LIMITS = [
                    {
                        "type": "user",
                        "name": spawner_inst.user.name,
                        "limits": {"cpu_limit": 3},
                    }
                ]
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.cpu_limit == 3

            def test_user_name_matches_mem_limit(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                constants.RESOURCE_LIMITS = [
                    {
                        "type": "user",
                        "name": spawner_inst.user.name,
                        "limits": {"mem_limit": "5M"},
                    }
                ]
                spawner_inst.run_pre_spawn_hook()
                assert spawner_inst.mem_limit == 5 * 1024**2

            def test_user_name_matches_gpu_ids_no_count(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                constants.RESOURCE_LIMITS = [
                    {
                        "type": "user",
                        "name": spawner_inst.user.name,
                        "limits": {"gpu_ids": [1, 2, 3]},
                    }
                ]
                spawner_inst.run_pre_spawn_hook()
                device_ids = spawner_inst.extra_host_config["device_requests"][0].device_ids
                assert len(device_ids) == 1
                assert device_ids[0] in [1, 2, 3]

            def test_user_name_matches_gpu_ids_with_count(self, spawner, constants, generate_spawner_inst):
                spawner_inst = generate_spawner_inst(spawner)
                constants.RESOURCE_LIMITS = [
                    {
                        "type": "user",
                        "name": spawner_inst.user.name,
                        "limits": {"gpu_ids": [1, 2, 3], "gpu_count": 2},
                    }
                ]
                spawner_inst.run_pre_spawn_hook()
                device_ids = spawner_inst.extra_host_config["device_requests"][0].device_ids
                assert len(device_ids) == 2
                assert set(device_ids) < {1, 2, 3}

            def test_additional_resource_limits(self, spawner, constants, generate_spawner_inst):
                mock = Mock()
                spawner_inst = generate_spawner_inst(spawner)
                spawner_inst.resource_limit_callbacks["test_limit"] = mock
                constants.RESOURCE_LIMITS = [
                    {
                        "type": "user",
                        "name": spawner_inst.user.name,
                        "limits": {"test_limit": 22},
                    }
                ]
                spawner_inst.run_pre_spawn_hook()
                assert mock.call_args == ((spawner_inst, 22),)
        
        class TestAdditionalPreSpawnHooks:

            def test_custom_pre_spawn_hook(self, spawner, generate_spawner_inst):
                mock = Mock()
                spawner_inst = generate_spawner_inst(spawner)
                spawner_inst.pre_spawn_hooks.append(mock)
                spawner_inst.run_pre_spawn_hook()
                assert mock.call_args == ((spawner_inst,),)

# @pytest.mark.asyncio
class TestMagpieAuthenticator:
    @pytest.fixture
    def authenticator(self, mock_env):
        yield reload(importlib.import_module("jupyterhub_custom.magpie_authenticator"))

    class TestLogoutHandler:
        @pytest.fixture
        def logout_handler(self, authenticator):
            handler = MagicMock()
            handler.handle_logout = lambda: authenticator.MagpieLogoutHandler.handle_logout(handler)
            handler.authenticator = authenticator.MagpieAuthenticator()
            handler.request = MagicMock()
            handler.request.cookies = {"cookie1": Morsel()}
            yield handler

        def test_handle_logout(self, logout_handler, constants):
            with patch("requests.get") as mock:
                mock.return_value.ok = True
                mock.return_value.headers = {"Set-Cookie": "logout-cookie"}
                asyncio.run(logout_handler.handle_logout())
                assert mock.call_count == 1
                assert mock.call_args.args == (logout_handler.authenticator.magpie_url + "/signout",)
                assert mock.call_args.kwargs == {
                    "cookies": {"cookie1": None},
                    "headers": {"Host": constants.BIRDHOUSE_FQDN_PUBLIC},
                }
                assert logout_handler.set_header.call_args.args == ("Set-Cookie", "logout-cookie")

    class TestAuthenticator:
        @pytest.fixture
        def magpie_authenticator(self, authenticator):
            yield authenticator.MagpieAuthenticator()

        def test_public_fqdn(self, magpie_authenticator, constants):
            assert magpie_authenticator.public_fqdn == constants.BIRDHOUSE_FQDN_PUBLIC

        def test_authorization_url(self, magpie_authenticator, constants):
            assert magpie_authenticator.authorization_url == constants.JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL

        def test_enable_auth_state(self, magpie_authenticator, constants):
            assert magpie_authenticator.enable_auth_state == constants.JUPYTERHUB_CRYPT_KEY_IS_SET

        def test_refresh_pre_spawn(self, magpie_authenticator, constants):
            assert magpie_authenticator.refresh_pre_spawn == constants.JUPYTERHUB_CRYPT_KEY_IS_SET

        def test_get_handlers(self, magpie_authenticator, authenticator):
            assert magpie_authenticator.get_handlers({}) == [("/logout", authenticator.MagpieLogoutHandler)]

        @pytest.mark.asyncio
        class TestAuthenticate:
            @pytest.fixture(autouse=True)
            def auth_mock(self):
                with patch("requests.post") as mock:
                    yield mock

            @pytest.fixture(autouse=True)
            def authz_mock(self):
                with patch("requests.get") as mock:
                    mock.side_effect = [
                        Mock(),
                    ]

            @pytest.fixture
            def auth_data(self):
                yield {"username": "user1", "password": "pwd123"}

            async def test_post_username_password(self, auth_mock, auth_data, magpie_authenticator):
                with patch("requests.get"):
                    await magpie_authenticator.authenticate(MagicMock(), auth_data)
                assert auth_mock.call_args.args == (magpie_authenticator.magpie_url + "/signin",)
                assert auth_mock.call_args.kwargs["data"] == {
                    "user_name": auth_data["username"],
                    "password": auth_data["password"],
                    "provider_name": magpie_authenticator.default_provider,
                }

            async def test_bad_initial_response(self, auth_mock, auth_data, magpie_authenticator):
                auth_mock.return_value.ok = False
                assert await magpie_authenticator.authenticate(MagicMock(), auth_data) is None

            async def test_not_authenticated(self, auth_mock, auth_data, magpie_authenticator):
                auth_mock.return_value.ok = False
                assert await magpie_authenticator.authenticate(MagicMock(), auth_data) is None

            async def test_not_authorized(self, auth_mock, auth_data, magpie_authenticator):
                auth_mock.return_value.ok = True
                with patch("requests.get") as authz_mock:
                    authz_mock.return_value.ok = False
                    assert await magpie_authenticator.authenticate(MagicMock(), auth_data) is None

            async def test_no_userdata(self, auth_mock, auth_data, magpie_authenticator):
                auth_mock.return_value.ok = True
                with patch("requests.get") as authz_mock:
                    first_resp, second_resp = Mock(), Mock()
                    first_resp.ok = True
                    second_resp.ok = False
                    authz_mock.side_effect = [first_resp, second_resp]
                    assert await magpie_authenticator.authenticate(MagicMock(), auth_data) is None

            async def test_no_check_authorized(self, auth_mock, auth_data, magpie_authenticator):
                auth_mock.return_value.ok = True
                magpie_authenticator.authorization_url = ""
                with patch("requests.get") as authz_mock:
                    authz_mock.return_value.ok = True
                    assert await magpie_authenticator.authenticate(MagicMock(), auth_data) is not None

            async def test_return_name_group(self, auth_data, magpie_authenticator):
                with patch("requests.get") as authz_mock:
                    first_resp, second_resp = Mock(), Mock()
                    second_resp.json.return_value = {
                        "user": {"user_name": "user1", "group_names": ["group1", "group2"]}
                    }
                    authz_mock.side_effect = [first_resp, second_resp]
                    data = await magpie_authenticator.authenticate(MagicMock(), auth_data)
                    data["name"] == "user1"
                    data["groups"] == ["group1", "group2"]

            async def test_return_magpie_cookies_if_authstate(self, auth_mock, auth_data, magpie_authenticator):
                with patch("requests.get") as authz_mock:
                    first_resp, second_resp = Mock(), Mock()
                    second_resp.json.return_value = {
                        "user": {"user_name": "user1", "group_names": ["group1", "group2"]}
                    }
                    authz_mock.side_effect = [first_resp, second_resp]
                    auth_mock.return_value.cookies = requests.cookies.RequestsCookieJar()
                    auth_mock.return_value.cookies.set("test", "value")
                    magpie_authenticator.enable_auth_state = True
                    data = await magpie_authenticator.authenticate(MagicMock(), auth_data)
                    assert data["auth_state"] == {"magpie_cookies": {"test": "value"}}

            async def test_no_return_magpie_cookies_if_no_authstate(self, auth_mock, auth_data, magpie_authenticator):
                with patch("requests.get") as authz_mock:
                    first_resp, second_resp = Mock(), Mock()
                    second_resp.json.return_value = {
                        "user": {"user_name": "user1", "group_names": ["group1", "group2"]}
                    }
                    authz_mock.side_effect = [first_resp, second_resp]
                    auth_mock.return_value.cookies = requests.cookies.RequestsCookieJar()
                    auth_mock.return_value.cookies.set("test", "value")
                    magpie_authenticator.enable_auth_state = False
                    data = await magpie_authenticator.authenticate(MagicMock(), auth_data)
                    assert "auth_state" not in data

            async def test_set_cookie(self, auth_mock, auth_data, magpie_authenticator):
                with patch("requests.get") as authz_mock:
                    first_resp, second_resp = Mock(), Mock()
                    second_resp.json.return_value = {
                        "user": {"user_name": "user1", "group_names": ["group1", "group2"]}
                    }
                    authz_mock.side_effect = [first_resp, second_resp]
                    handler = Mock()
                    auth_mock.return_value.cookies = requests.cookies.RequestsCookieJar()
                    auth_mock.return_value.cookies.set("test", "value")
                    await magpie_authenticator.authenticate(handler, auth_data)
                    assert handler.set_cookie.call_args.kwargs["name"] == "test"
                    assert handler.set_cookie.call_args.kwargs["value"] == "value"
                    assert handler.set_cookie.call_args.kwargs["domain"] == "example.com"

        @pytest.mark.asyncio
        class TestRefreshUser:
            @pytest.fixture(autouse=True)
            def authz_mock(self):
                with patch("requests.get") as mock:
                    yield mock

            async def test_auth_state_disabled(self, magpie_authenticator):
                magpie_authenticator.enable_auth_state = False
                magpie_authenticator.authorization_url = "http://example.com/auth/test"
                user = Mock()
                user.get_auth_state = AsyncMock(return_value={"something": "here"})
                assert await magpie_authenticator.refresh_user(user) is True

            async def test_auth_state_unset(self, magpie_authenticator):
                magpie_authenticator.enable_auth_state = True
                magpie_authenticator.authorization_url = "http://example.com/auth/test"
                user = Mock()
                user.get_auth_state = AsyncMock(return_value=None)
                assert await magpie_authenticator.refresh_user(user) is True

            async def test_authorization_url_unset(self, magpie_authenticator):
                magpie_authenticator.enable_auth_state = True
                magpie_authenticator.authorization_url = ""
                user = Mock()
                user.get_auth_state = AsyncMock(return_value={"something": "here"})
                assert await magpie_authenticator.refresh_user(user) is True

            async def test_magpie_cookies_valid(self, authz_mock, magpie_authenticator):
                magpie_authenticator.enable_auth_state = True
                magpie_authenticator.authorization_url = "http://example.com/auth/test"
                user = Mock()
                user.get_auth_state = AsyncMock(return_value={"magpie_cookies": {"test": "cookie"}})
                authz_mock.return_value.ok = True
                assert await magpie_authenticator.refresh_user(user) is True

            async def test_magpie_cookies_invalid(self, authz_mock, magpie_authenticator):
                magpie_authenticator.enable_auth_state = True
                magpie_authenticator.authorization_url = "http://example.com/auth/test"
                user = Mock()
                user.get_auth_state = AsyncMock(return_value={"magpie_cookies": {"test": "cookie"}})
                authz_mock.return_value.ok = False
                assert await magpie_authenticator.refresh_user(user) is False

            async def test_magpie_cookies_invalid_clear_login_cookies(self, authz_mock, magpie_authenticator):
                magpie_authenticator.enable_auth_state = True
                magpie_authenticator.authorization_url = "http://example.com/auth/test"
                user = Mock()
                user.get_auth_state = AsyncMock(return_value={"magpie_cookies": {"test": "cookie"}})
                authz_mock.return_value.ok = False
                handler = Mock()
                await magpie_authenticator.refresh_user(user, handler)
                assert handler.clear_login_cookie.call_count == 1

        @pytest.mark.asyncio
        class TestPreSpawnStart:
            async def test_auth_state_is_set(self, magpie_authenticator):
                user = Mock()
                spawner = Mock()
                spawner.environment = {}
                user.get_auth_state = AsyncMock(return_value={"magpie_cookies": {"test": "cookie"}})
                await magpie_authenticator.pre_spawn_start(user, spawner)
                assert spawner.environment["MAGPIE_COOKIES"] == '{"test": "cookie"}'

            async def test_auth_state_is_not_set(self, magpie_authenticator):
                user = Mock()
                spawner = Mock()
                spawner.environment = {}
                user.get_auth_state = AsyncMock(return_value=None)
                await magpie_authenticator.pre_spawn_start(user, spawner)
                assert "MAGPIE_COOKIES" not in spawner.environment
