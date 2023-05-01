from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from tornado import gen, web

# TODO: add this to
#  github.com/Ouranosinc/jupyterhub/blob/master/jupyterhub_magpie_authenticator/jupyterhub_magpie_authenticator.py
#  and remove this from here once that is updated


class MagpieLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        remote_user = self.request.headers.get(header_name, "")
        if remote_user == "":
            raise web.HTTPError(401)

        user = self.user_from_username(remote_user)
        self.set_login_cookie(user)
        next_url = self.get_next_url(user)
        self.redirect(next_url)


class MagpieAuthenticator(Authenticator):
    """
    Accept the authenticated username from the X-REMOTE-USER HTTP header.
    """
    header_name = 'X-REMOTE-USER'  # header set by twitcher
    auto_login = True

    def get_handlers(self, app):
        return [
            (r'/login', MagpieLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
