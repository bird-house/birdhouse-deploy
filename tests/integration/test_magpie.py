import pytest
import requests

pytestmark = pytest.mark.minimal


@pytest.fixture(scope="module")
def magpie_url(birdhouse_url):
    return f"{birdhouse_url}/magpie"


def test_magpie_is_running(magpie_url):
    requests.get(magpie_url).raise_for_status()


def test_admin_can_log_in(magpie_url, stack_env):
    response = requests.post(
        f"{magpie_url}/signin",
        data={
            "user_name": stack_env["MAGPIE_ADMIN_USERNAME"],
            "password": stack_env["MAGPIE_ADMIN_PASSWORD"],
        },
    )
    response.raise_for_status()
    assert any(cookie.domain == stack_env["BIRDHOUSE_FQDN_PUBLIC"] for cookie in response.cookies)
