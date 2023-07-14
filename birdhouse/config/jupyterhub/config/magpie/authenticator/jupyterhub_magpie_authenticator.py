from traitlets import Unicode
from jupyterhub.auth import Authenticator
from tornado import gen
import requests

# TODO: add this to
#  github.com/Ouranosinc/jupyterhub/blob/master/jupyterhub_magpie_authenticator/jupyterhub_magpie_authenticator.py
#  and remove this from here once that is updated

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

    @gen.coroutine
    def authenticate(self, handler, data):
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
