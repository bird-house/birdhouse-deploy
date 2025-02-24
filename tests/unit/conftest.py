import pytest


@pytest.fixture(scope="module")
def root_dir(request):
    # implement this for every testing subfolder
    yield request.path.parent.parent.parent


@pytest.fixture(scope="module")
def local_env_file(root_dir):
    yield root_dir / "tests" / "test.env"
