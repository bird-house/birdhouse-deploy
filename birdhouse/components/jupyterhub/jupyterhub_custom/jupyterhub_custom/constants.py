import os

import yaml

from ._typing import LimitRule

# Constants that are non-configurable

NOTEBOOK_DIR: str = "/notebook_dir"
USER_KERNELS_DIR: str = "/var/tmp/user-kernels"
CONTAINER_WORKSPACE_DIR: str = os.path.join(NOTEBOOK_DIR, "writable-workspace")
CONTAINER_HOME_DIR: str = os.path.join(CONTAINER_WORKSPACE_DIR, ".home")
CONTAINER_GDRIVE_SETTINGS_PATH: str = os.path.join(
    CONTAINER_HOME_DIR,
    ".jupyter/lab/user-settings/@jupyterlab/google-drive/drive.jupyterlab-settings",
)

# Constants that are set based on the current environment.
# Please add all future environment variable changes here so that we can easily keep track of them in one place.

JUPYTERHUB_DATA_DIR: str = os.environ["JUPYTERHUB_USER_DATA_DIR"]
WORKSPACE_DIR: str = os.environ["WORKSPACE_DIR"]
HOST_USER_DATA_DIR: str = os.path.join(WORKSPACE_DIR, "{username}")
HOST_GDRIVE_SETTINGS_PATH: str = os.environ["JUPYTER_GOOGLE_DRIVE_SETTINGS"]
RESOURCE_LIMITS: LimitRule = yaml.safe_load(os.getenv("JUPYTERHUB_RESOURCE_LIMITS") or "[]")
README: str = os.getenv("JUPYTERHUB_README", "")
JUPYTER_IDLE_SERVER_CULL_TIMEOUT: int = int(os.getenv("JUPYTER_IDLE_SERVER_CULL_TIMEOUT") or 0)
JUPYTER_IDLE_KERNEL_CULL_TIMEOUT: int = int(os.getenv("JUPYTER_IDLE_KERNEL_CULL_TIMEOUT") or 0)
JUPYTER_IDLE_KERNEL_CULL_INTERVAL: int = int(os.getenv("JUPYTER_IDLE_KERNEL_CULL_INTERVAL") or 0)
BIRDHOUSE_FQDN_PUBLIC: str = os.environ["BIRDHOUSE_FQDN_PUBLIC"]
JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL: str = os.getenv("JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL", "")
JUPYTERHUB_CRYPT_KEY_IS_SET: bool = bool(os.getenv("JUPYTERHUB_CRYPT_KEY"))
JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE: int = int(os.getenv("JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE") or 0)
JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES: list[str] = os.environ["JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES"].split()
JUPYTERHUB_IMAGE_SELECTION_NAMES: list[str] = os.environ["JUPYTERHUB_IMAGE_SELECTION_NAMES"].split()
JUPYTERHUB_ALLOWED_IMAGES: dict[str, str] = yaml.safe_load(os.getenv("JUPYTERHUB_ALLOWED_IMAGES", ""))
DOCKER_NETWORK_NAME: str = os.environ["DOCKER_NETWORK_NAME"]
BIRDHOUSE_HOST_URL: str = f"{os.environ['BIRDHOUSE_PROXY_SCHEME']}://{BIRDHOUSE_FQDN_PUBLIC}"
PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR: str = os.getenv("PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR", "")
COWBIRD_ENABLED: bool = WORKSPACE_DIR != JUPYTERHUB_DATA_DIR
JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS: bool = os.getenv("JUPYTERHUB_MOUNT_IMAGE_SPECIFIC_NOTEBOOKS") == "true"
USER_WORKSPACE_UID: str = os.environ["USER_WORKSPACE_UID"]
USER_WORKSPACE_GID: str = os.environ["USER_WORKSPACE_GID"]
JUPYTER_DEMO_USER: str = os.environ["JUPYTER_DEMO_USER"]
JUPYTER_DEMO_USER_CPU_LIMIT: float = float(os.environ["JUPYTER_DEMO_USER_CPU_LIMIT"])
JUPYTER_DEMO_USER_MEM_LIMIT: str = os.environ["JUPYTER_DEMO_USER_MEM_LIMIT"]
JUPYTERHUB_ADMIN_GROUP_NAME: str = os.environ["JUPYTERHUB_ADMIN_GROUP_NAME"]
JUPYTERHUB_DOCKER_EXTRA_HOSTS: dict = dict(
    host_mapping.split(":") for host_mapping in os.getenv("JUPYTERHUB_DOCKER_EXTRA_HOSTS", "").split()
)

# The following constants have lowercase variable names for backwards compatibility
# in case any legacy code in JUPYTERHUB_CONFIG_OVERRIDE uses these variables.
#
# These variables are included in the __all__ variable so that they can be
# be imported with a star import in jupyterhub_config.py
#
# TODO: update legacy JUPYTERHUB_CONFIG_OVERRIDE values to use uppercase versions of these
#       variables (see above) and deprecate the code below this:

notebook_dir = NOTEBOOK_DIR
jupyterhub_data_dir = JUPYTERHUB_DATA_DIR
container_workspace_dir = CONTAINER_WORKSPACE_DIR
container_home_dir = CONTAINER_HOME_DIR
user_kernels_dir = USER_KERNELS_DIR
host_user_data_dir = HOST_USER_DATA_DIR
container_gdrive_settings_path = CONTAINER_GDRIVE_SETTINGS_PATH
host_gdrive_settings_path = HOST_GDRIVE_SETTINGS_PATH
resource_limits = RESOURCE_LIMITS
readme = README
jupyter_idle_server_cull_timeout = JUPYTER_IDLE_SERVER_CULL_TIMEOUT
jupyter_idle_kernel_cull_timeout = JUPYTER_IDLE_KERNEL_CULL_TIMEOUT
jupyter_idle_kernel_cull_interval = JUPYTER_IDLE_KERNEL_CULL_INTERVAL

__all__ = [
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
