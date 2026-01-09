import os
import random
import subprocess
from typing import Any

import docker
from dockerspawner import DockerSpawner
from traitlets import default

from . import constants


class CustomDockerSpawner(DockerSpawner):
    """Customizations on top of the DockerSpawner class for birdhouse."""

    # The following values override defaults in the DockerSpawner base class.
    # See the DockerSpawner documentation for more details:
    # https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html#module-0

    @default("image")
    def _default_image(self) -> str:
        return constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES[0]  # Selects the first image from the list by default

    @default("use_internal_ip")
    def _default_use_internal_ip(self) -> bool:
        return True

    @default("network_name")
    def _default_network_name(self) -> str:
        return constants.DOCKER_NETWORK_NAME

    @default("environment")
    def _default_environment(self) -> dict[str, str]:
        return {
            "HOME": constants.CONTAINER_HOME_DIR,
            # Adds a custom path that jupyterlab will use to search for kernels so that
            # user-generated kernels can be detected by jupyterlab (the default location
            # in the home directory is not visible to jupyterlab for some reason).
            # See c.DockerSpawner.post_start_cmd for more info.
            "JUPYTER_PATH": constants.USER_KERNELS_DIR,
            # https://docs.bokeh.org/en/latest/docs/user_guide/jupyter.html#jupyterhub
            # Issue https://github.com/bokeh/bokeh/issues/12090
            # Post on Panel forum:
            # https://discourse.holoviz.org/t/how-to-customize-the-display-url-from-panel-serve-for-use-behind-jupyterhub-with-jupyter-server-proxy/3571
            # Issue about Panel Preview: https://github.com/holoviz/panel/issues/3440
            "BIRDHOUSE_HOST_URL": constants.BIRDHOUSE_HOST_URL,
            # https://docs.dask.org/en/stable/configuration.html
            # https://jupyterhub-on-hadoop.readthedocs.io/en/latest/dask.html
            "DASK_DISTRIBUTED__DASHBOARD__LINK": (
                constants.BIRDHOUSE_HOST_URL + "{JUPYTERHUB_SERVICE_PREFIX}proxy/{port}/status"
            ),
        }

    @default("volumes")
    def _default_volumes(self) -> dict[str, str]:
        """
        Return a dictionary containing volume mount information.

        This is used to set CustomDockerSpawner.volumes
        """
        volumes = {constants.HOST_USER_DATA_DIR: constants.CONTAINER_WORKSPACE_DIR}
        if constants.COWBIRD_ENABLED:
            volumes[os.path.join(constants.JUPYTERHUB_DATA_DIR, "{username}")] = {
                "bind": os.path.join(constants.JUPYTERHUB_DATA_DIR, "{username}"),
                "mode": "rw",
            }
            volumes[os.path.join(constants.WORKSPACE_DIR, constants.PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR)] = {
                "bind": os.path.join(
                    constants.NOTEBOOK_DIR,
                    constants.PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR,
                ),
                "mode": "ro",
            }
        if constants.HOST_GDRIVE_SETTINGS_PATH:
            volumes[constants.HOST_GDRIVE_SETTINGS_PATH] = {
                "bind": constants.CONTAINER_GDRIVE_SETTINGS_PATH,
                "mode": "ro",
            }
        if constants.README:
            volumes[constants.README] = {
                "bind": os.path.join(constants.NOTEBOOK_DIR, "README.ipynb"),
                "mode": "ro",
            }
        return volumes

    @default("remove")
    def _default_remove(self) -> bool:
        """Delete containers when servers are stopped."""
        return True

    @default("pull_policy")
    def _default_pull_policy(self) -> str:
        """
        Image pull policy.

        Default is always to support images not using pinned version.
        """
        return "always"

    @default("args")
    def _default_args(self) -> list[str]:
        """
        Return a list containing extra args used to call the spawned singleuser server.

        This is used to set CustomDockerSpawner.args
        """
        args = [
            # Allow non-empty directory deletion which enable recursive dir deletion.
            # https://jupyter-server.readthedocs.io/en/latest/other/full-config.html
            "--FileContentsManager.always_delete_dir=True",
        ]
        if constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT:
            # Timeout (in seconds) to shut down the user server when no kernels or terminals
            # are running and there is no activity. If undefined or set to zero, the feature will not be enabled.
            args.append(f"--NotebookApp.shutdown_no_activity_timeout={constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT}")
        # Timeout (in seconds) after which individual user kernels/terminals are considered idle and ready to be culled.
        kernel_cull_timeout = constants.JUPYTER_IDLE_KERNEL_CULL_TIMEOUT
        # Interval (in seconds) on which to check for idle kernels exceeding the cull timeout value.
        kernel_cull_interval = constants.JUPYTER_IDLE_KERNEL_CULL_INTERVAL
        if kernel_cull_timeout:
            if not kernel_cull_interval or kernel_cull_interval > kernel_cull_timeout:
                kernel_cull_interval = max(1, int(kernel_cull_timeout / 2))
            args.extend(
                [
                    f"--MappingKernelManager.cull_idle_timeout={kernel_cull_timeout}",
                    f"--MappingKernelManager.cull_interval={kernel_cull_interval}",
                    f"--TerminalManager.cull_inactive_timeout={kernel_cull_timeout}",
                    f"--TerminalManager.cull_interval={kernel_cull_interval}",
                ]
            )
        # Culling kernels which have one or more connections for idle but open notebooks and/or terminals.
        # Otherwise, browser tabs, notebooks and terminals all have to be closed for culling to work.
        if constants.JUPYTER_IDLE_SERVER_CULL_TIMEOUT or kernel_cull_timeout:
            args.extend(
                [
                    "--MappingKernelManager.cull_connected=True",
                    "--TerminalManager.cull_connected=True",
                ]
            )

        return args

    @default("extra_host_config")
    def _default_extra_host_config(self) -> dict[str, Any]:
        """Return extra host configuration dictionary."""
        return {
            # start init pid 1 process to reap defunct processes
            "init": True,
            # Note that JUPYTERHUB_DOCKER_EXTRA_HOSTS may be set by default in the local-dev-test component
            "extra_hosts": constants.JUPYTERHUB_DOCKER_EXTRA_HOSTS,
        }

    @default("post_start_cmd")
    def _default_post_start_cmd(self) -> str:
        """
        Return a post start command.

        This ensures that the docker healthchecks pass for the jupyterlab containers
        The healthchecks assume that the jupyter data directory is in /home/$NB_USER/.local
        regardless of the value of $HOME.
        It also makes a symlink between the kernels directory in the user space to another
        location outside of the home directory. This is because jupyterlab is currently unable
        to detect kernels inside the user's home directory for some reason.
        This also removes any old server metadata files which may not be cleaned up if the container
        exits unexpectedly. This is necessary to ensure that the healthcheck can detect the correct
        hostname of the jupyterlab server (this changes every time a new container is created).
        """
        post_start_command = (
            "ln -s $HOME/.local /home/$NB_USER/.local; "
            f"mkdir -p {constants.USER_KERNELS_DIR}; "
            f"ln -s $HOME/.local/share/jupyter/kernels {constants.USER_KERNELS_DIR}/kernels; "
            "rm $HOME/.local/share/jupyter/runtime/jpserver-*.json"
        )
        return f"sh -c '{post_start_command}'"

    @default("allowed_images")
    def _default_allowed_images(self) -> list[str] | dict[str, str]:
        """
        Return a dictionary or list containing images that a user is allowed to select.

        This is used to set CustomDockerSpawner.allowed_images
        """
        images = constants.JUPYTERHUB_ALLOWED_IMAGES
        if images is None:
            if constants.JUPYTERHUB_IMAGE_SELECTION_NAMES:
                images = dict(
                    zip(constants.JUPYTERHUB_IMAGE_SELECTION_NAMES, constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES)
                )
            else:
                images = constants.JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES
        if len(images) == 1:
            # do not allow user to select an image if there is only one option
            return []
        return images

    # The following values override defaults in the Spawner base class.
    # See the Spawner documentation for more details:
    # https://jupyterhub.readthedocs.io/en/latest/reference/api/spawner.html#jupyterhub.spawner.Spawner

    @default("notebook_dir")
    def _default_notebook_dir(self) -> str:
        """Return notebook directory path."""
        return constants.NOTEBOOK_DIR

    @default("disable_user_config")
    def _default_disable_user_config(self) -> bool:
        """Disable per-user configuration of single-user servers."""
        return True

    @default("default_url")
    def _default_default_url(self) -> str:
        """Set the URL the single-user server should start in."""
        return "/lab"

    @default("debug")
    def _default_debug(self) -> bool:
        """Debug log output."""
        return True

    @default("http_timeout")
    def _default_http_timeout(self) -> int:
        """Timeout (in seconds) before giving up on a spawned HTTP server."""
        return 60

    @default("start_timeout")
    def _default_start_timeout(self) -> int:
        """Timeout (in seconds) before giving up on starting of single-user server."""
        return 120

    @property
    def escaped_name(self) -> str:
        """
        Return the username without escaping.

        This ensures that mounted directories on the host machine are discovered properly since
        we expect the username to match the username set by Magpie.
        """
        return self.user.name

    def __create_tutorial_notebook_hook(self) -> None:
        """Mount tutorial notebooks as volumes based on the selected singleuser jupyterlab image."""
        container_tutorial_dir = os.path.join(constants.NOTEBOOK_DIR, "tutorial-notebooks")
        if constants.JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS:
            host_tutorial_dir = os.path.join(
                constants.JUPYTERHUB_DATA_DIR,
                "tutorial-notebooks-specific-images",
            )

            # Mount a volume with a tutorial-notebook subfolder corresponding to the image name, if it exists
            # The names are defined in the JUPYTERHUB_IMAGE_SELECTION_NAMES variable.
            image_name = self.user_options["image"]
            host_tutorial_subdir = os.path.join(host_tutorial_dir, image_name)
            if not os.path.isdir(host_tutorial_subdir):
                # Try again, removing any colons and any following text. Useful if the image name contains
                # the version number, which should not be used in the directory name.
                host_tutorial_subdir = os.path.join(host_tutorial_dir, image_name.split(":")[0])
            if os.path.isdir(host_tutorial_subdir):
                self.volumes[host_tutorial_subdir] = {
                    "bind": container_tutorial_dir,
                    "mode": "ro",
                }
        else:
            # Mount the entire tutorial-notebooks directory
            self.volumes[os.path.join(constants.JUPYTERHUB_DATA_DIR, "tutorial-notebooks")] = {
                "bind": container_tutorial_dir,
                "mode": "ro",
            }

    def __create_dir_hook(self) -> None:
        """Create user workspace directories on the host and update permissions if necessary."""
        username = self.user.name
        jupyterhub_user_dir = os.path.join(constants.JUPYTERHUB_DATA_DIR, username)

        if not os.path.exists(jupyterhub_user_dir):
            os.mkdir(jupyterhub_user_dir, 0o755)

        subprocess.call(
            [
                "chown",
                "-R",
                f"{constants.USER_WORKSPACE_UID}:{constants.USER_WORKSPACE_GID}",
                jupyterhub_user_dir,
            ]
        )

        if constants.COWBIRD_ENABLED:
            # Case for cowbird setup. The workspace directory should also have the user's ownership,
            # to have working volume mounts with the DockerSpawner.
            workspace_user_dir = os.path.join(constants.WORKSPACE_DIR, username)
            if not os.path.exists(workspace_user_dir):
                os.symlink(jupyterhub_user_dir, workspace_user_dir, target_is_directory=True)
            subprocess.call(
                [
                    "chown",
                    f"{constants.USER_WORKSPACE_UID}:{constants.USER_WORKSPACE_GID}",
                    workspace_user_dir,
                ]
            )

    def __limit_resource_hook(self) -> None:
        """Apply resource limits for the singleuser jupyterlab container."""
        if self.user.name == constants.JUPYTER_DEMO_USER:
            # Restrict resources for the public demo user
            # CPU limit, seems not honored by DockerSpawner
            self.cpu_limit = constants.JUPYTER_DEMO_USER_CPU_LIMIT
            self.mem_limit = constants.JUPYTER_DEMO_USER_MEM_LIMIT

        user_groups = {g.name for g in self.user.groups}
        gpu_ids = []
        gpu_count = 1
        for rule in constants.RESOURCE_LIMITS:
            rule_type = rule["type"]
            name = rule["name"]
            if rule_type == "user" and name == self.user.name or rule_type == "group" and name in user_groups:
                for limit, value in rule["limits"].items():
                    if limit == "cpu_limit":
                        self.cpu_limit = value
                    elif limit == "mem_limit":
                        self.mem_limit = value
                    elif limit == "gpu_ids":
                        gpu_ids = value
                    elif limit == "gpu_count":
                        gpu_count = value
        if gpu_ids:
            # randomly assign GPUs in an attempt to evenly distribute GPU resources
            random.shuffle(gpu_ids)
            gpu_ids = gpu_ids[:gpu_count]
            self.extra_host_config["device_requests"] = [
                docker.types.DeviceRequest(device_ids=gpu_ids, capabilities=[["gpu"]])
            ]

    def pre_spawn_hook(self, _spawner: "CustomDockerSpawner") -> None:
        """Run before spawning a singleuser jupyterlab server."""
        self.__create_dir_hook()
        self.__limit_resource_hook()
        self.__create_tutorial_notebook_hook()
