import json

import requests
from jupyterhub.app import JupyterHub
from jupyterhub.auth import Authenticator
from jupyterhub.handlers.base import BaseHandler
from jupyterhub.handlers.login import LogoutHandler
from jupyterhub.spawner import Spawner
from jupyterhub.user import User
from traitlets import Unicode, default

from . import constants


class MagpieLogoutHandler(LogoutHandler):
    """Logout Handler that also logs the user out of magpie when logging out of jupyterhub."""

    async def handle_logout(self) -> None:
        """Logout of Magpie."""
        cookies = {key: morsel.coded_value for key, morsel in self.request.cookies.items()}
        signout_url = self.authenticator.magpie_url.rstrip("/") + "/signout"
        response = requests.get(
            signout_url,
            cookies=cookies,
            headers={"Host": self.authenticator.public_fqdn},
        )
        if response.ok and "Set-Cookie" in response.headers:
            self.set_header("Set-Cookie", response.headers["Set-Cookie"])


class MagpieAuthenticator(Authenticator):
    """Authenticate to JupyterHub using Magpie.

    To use this authenticator, set the following parameters in the `jupyterhub_config.py` file:
     - c.JupyterHub.authenticator_class = 'jupyterhub_magpie_authenticator.MagpieAuthenticator'
     - c.MagpieAuthenticator.magpie_url = "magpie:2000" # url where magpie is running (does not need to be public)
     - c.MagpieAuthenticator.public_fqdn = "www.example.com"  # fqdn of server where magpie is running

    You may also optionally choose to set an `authorization_url` which is a URL that can be used to check whether the
    user logged in to Magpie has permission to access jupyterhub:
     - c.MagpieAuthenticator.authorization_url = "http://twitcher:8000/ows/verify/jupyterhub"

    If `authorization_url` is set, then setting `enable_auth_state` will enable jupyterhub to store the user's magpie
    cookies. This will allow the `refresh_user` method to periodically check whether the user is still authorized and
    will attempt to log them out of jupyterhub if not.
    These cookie values will also be available in the spawned jupyterlab server by accessing the `MAGPIE_COOKIES`
    environment variable. This variable will contain a JSON object where keys are the cookie names and values are the
    cookie content.

    If `authorization_url` and `enable_auth_state` are set, then you may also be interested in setting the
    `refresh_pre_spawn` and `auth_refresh_age` variables. See the jupyterhub documentation for more details.

    The `manage_groups` attribute tells Jupyterhub that the Authenticator can set group memberships based on
    the values returned by the `authenticate` method. This is True by default for this Authenticator.
    """

    default_provider = "ziggurat"
    magpie_url = Unicode(
        default_value="http://magpie:2001",
        config=True,
        help="Magpie endpoint to signin to",
    )
    public_fqdn = Unicode(
        default_value=constants.BIRDHOUSE_FQDN_PUBLIC,
        config=True,
        help="Public fully qualified domain name. Used to set the magpie login cookie.",
    )
    authorization_url = Unicode(
        default_value=constants.JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL,
        config=True,
        help="optional URL that can be used to check whether the user logged in to Magpie has permission to access "
        "jupyterhub",
    )

    # The following values override defaults in the Authenticator base class.
    # See the Authenticator documentation for more details:
    # https://jupyterhub.readthedocs.io/en/latest/reference/api/auth.html#jupyterhub.auth.Authenticator

    @default("manage_groups")
    def _default_manage_groups(self) -> bool:
        return True

    @default("enable_auth_state")
    def _default_enable_auth_state(self) -> bool:
        return constants.JUPYTERHUB_CRYPT_KEY_IS_SET

    @default("refresh_pre_spawn")
    def _default_refresh_pre_spawn(self) -> bool:
        return constants.JUPYTERHUB_CRYPT_KEY_IS_SET

    @default("auth_refresh_age")
    def _default_auth_refresh_age(self) -> int:
        return constants.JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE

    @default("allow_all")
    def _default_allow_all(self) -> bool:
        """
        Allow all users who can authenticate through Magpie to log in to JupyterHub.

        This allows us to manage users on Magpie without having to also update the
        JupyterHub database manually to match Magpie permissions.

        Note that users on the blocked_users list will still be denied even though
        they can authenticate through Magpie.
        """
        return True

    @default("blocked_users")
    def _default_blocked_users(self) -> set:
        """Block user with known hardcoded public password or non real Jupyter users."""
        return {"authtest", "anonymous"}

    def get_handlers(self, app: JupyterHub) -> list[tuple[str, type[BaseHandler]]]:
        """Return any custom handlers the authenticator needs to register."""
        return [("/logout", MagpieLogoutHandler)]

    async def authenticate(self, handler: BaseHandler, data: dict) -> dict | None:
        """Authenticate a user with login form data."""
        signin_url = self.magpie_url.rstrip("/") + "/signin"
        userdata_url = self.magpie_url.rstrip("/") + "/users/current"

        post_data = {
            "user_name": data["username"],
            "password": data["password"],
            "provider_name": self.default_provider,
        }
        response = requests.post(signin_url, data=post_data)

        if response.ok:
            if self.authorization_url:
                auth_response = requests.get(self.authorization_url, cookies=response.cookies.get_dict())
                if not auth_response.ok:
                    return None
            userdata_response = requests.get(userdata_url, cookies=response.cookies.get_dict())
            if not userdata_response.ok:
                return None
            userdata = userdata_response.json()
            user_name = userdata["user"]["user_name"]
            groups = userdata["user"]["group_names"]
            for cookie in response.cookies:
                handler.set_cookie(
                    name=cookie.name,
                    value=cookie.value,
                    domain=self.public_fqdn,
                    expires=cookie.expires,
                    path=cookie.path,
                    secure=cookie.secure,
                )
            if self.enable_auth_state:
                return {
                    "name": user_name,
                    "groups": groups,
                    "auth_state": {"magpie_cookies": response.cookies.get_dict()},
                }
            else:
                return {"name": user_name, "groups": groups}

    async def refresh_user(self, user: User, handler: BaseHandler | None = None) -> bool:
        """Refresh auth data for a given user."""
        auth_state = await user.get_auth_state()
        if auth_state is None or not (self.authorization_url and self.enable_auth_state):
            # MagpieAuthenticator is not configured to re-check user authorization or the auth state
            # has not been persisted to the database yet.
            return True
        cookies = auth_state.get("magpie_cookies")
        if cookies:
            auth_response = requests.get(self.authorization_url, cookies=cookies)
            if auth_response.ok:
                return True
        if handler:
            handler.clear_login_cookie()
        return False

    async def pre_spawn_start(self, user: User, spawner: Spawner) -> None:
        """Call before spawning a user's server."""
        auth_state = await user.get_auth_state()
        if auth_state is None:
            # MagpieAuthenticator is not configured to store user authorization data or the auth state
            # has not been persisted to the database yet.
            return
        spawner.environment["MAGPIE_COOKIES"] = json.dumps(auth_state.get("magpie_cookies"))
