..
  TODO: add a description of this service


Jupyterhub as a service cannot use twitcher as a proxy due to the fact that twitcher is unable to set cookies (set by
the jupyterhub oauth2 service) on a browser. As a workaround, jupyterhub uses magpie to authenticate usernames and
passwords. Unfortunately, this means that users must log in to jupyter separately from magpie.
