import os
import pathlib
import pytest

# These are used for integration tests only but are defined here so that tests run from the top level tests/
# directory will execute without error.
def pytest_addoption(parser):
    parser.addoption(
        "--no-start-stack",
        action="store_true",
        help="Do not start the birdhouse stack or stop it afterwards. Assumes that the stack is already running",
    )
    parser.addoption(
        "--no-stop-stack",
        action="store_true",
        help="Do not stop the birdhouse stack at the end of the test run.",
    )
    parser.addoption(
        "--no-rm-data",
        action="store_true",
        help="Do not delete the temporary data persist directory at the end of the test run.",
    )
    parser.addoption(
        "--wait-for-healthy-timeout",
        action="store",
        default="60",
        help="Number of seconds to wait for the stack to be healthy after it starts up",
    )

@pytest.fixture(scope="module")
def root_dir(request):
    # implement this for every testing subfolder
    raise NotImplementedError


@pytest.fixture(scope="module")
def local_env_file(root_dir):
    yield pathlib.Path(
        os.getenv("TEST_BIRDHOUSE_LOCAL_ENV", root_dir / "tests" / "env.local.test")
    )
