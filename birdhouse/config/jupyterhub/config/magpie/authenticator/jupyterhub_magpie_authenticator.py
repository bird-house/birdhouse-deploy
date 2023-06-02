from traitlets import Unicode
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from tornado import gen, web
import requests

# TODO: add this to
#  github.com/Ouranosinc/jupyterhub/blob/master/jupyterhub_magpie_authenticator/jupyterhub_magpie_authenticator.py
#  and remove this from here once that is updated


class MagpieLoginHandler(BaseHandler):

    def get(self):
        cookies = {key: morsel.coded_value for key, morsel in self.request.cookies.items()}

        response = requests.get(self.authenticator.magpie_url.rstrip("/") + '/users/current', cookies=cookies)
        remote_user = response.json().get("user", {}).get("user_name")

        if not remote_user or remote_user in self.authenticator.blocked_users:
            raise web.HTTPError(401)

        user = self.user_from_username(remote_user)
        self.set_login_cookie(user)
        next_url = self.get_next_url(user)
        self.redirect(next_url)


class MagpieAuthenticator(Authenticator):
    """
    Accept the authenticated username from the X-REMOTE-USER HTTP header.
    """
    magpie_url = Unicode(
        default_value="https://www.example.com/magpie",
        config=True,
        help="Magpie endpoint to signin to"
    )
    auto_login = True

    def get_handlers(self, app):
        return [
            (r'/login', MagpieLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
