from traitlets import Unicode
from jupyterhub.auth import Authenticator
from jupyterhub.handlers.login import LogoutHandler
import requests


# TODO: add this to
#  github.com/Ouranosinc/jupyterhub/blob/master/jupyterhub_magpie_authenticator/jupyterhub_magpie_authenticator.py
#  and remove this from here once that is updated

class MagpieLogoutHandler(LogoutHandler):
    """
    Logout Handler that also logs the user out of magpie when logging out of jupyterhub.
    """
    async def handle_logout(self):
        cookies = {key: morsel.coded_value for key, morsel in self.request.cookies.items()}
        signout_url = self.authenticator.magpie_url.rstrip("/") + "/signout"
        response = requests.get(signout_url, cookies=cookies, headers={"Host": self.authenticator.public_fqdn})
        if response.ok and 'Set-Cookie' in response.headers:
            self.set_header("Set-Cookie", response.headers["Set-Cookie"])


class MagpieAuthenticator(Authenticator):
    """Authenticate to JupyterHub using Magpie.

    To use this authenticator, set the following parameters in the `jupyterhub_config.py` file:
     - c.JupyterHub.authenticator_class = 'jupyterhub_magpie_authenticator.MagpieAuthenticator'
     - c.MagpieAuthenticator.magpie_url = "https://www.example.com/magpie"
    """
    default_provider = "ziggurat"
    magpie_url = Unicode(
        default_value="https://www.example.com/magpie",
        config=True,
        help="Magpie endpoint to signin to"
    )
    public_fqdn = Unicode(
        config=True,
        help="Public fully qualified domain name. Used to set the magpie login cookie."
    )

    def get_handlers(self, app):
        return [
            ('/logout', MagpieLogoutHandler)
        ]

    async def authenticate(self, handler, data):
        signin_url = self.magpie_url.rstrip('/') + '/signin'

        post_data = {
            "user_name": data["username"],
            "password": data["password"],
            "provider_name": self.default_provider,
        }
        response = requests.post(signin_url, data=post_data)

        if response.ok:
            for cookie in response.cookies:
                handler.set_cookie(name=cookie.name,
                                   value=cookie.value,
                                   domain=self.public_fqdn,
                                   expires=cookie.expires,
                                   path=cookie.path,
                                   secure=cookie.secure)
            return data['username']
