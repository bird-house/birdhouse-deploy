import pytest
import sys
from pathlib import Path
import importlib.util


@pytest.fixture(scope="module")
def root_dir(request):
    # implement this for every testing subfolder
    yield request.path.parent.parent.parent


@pytest.fixture(scope="module")
def local_env_file(root_dir):
    yield root_dir / "tests" / "test.env"


@pytest.fixture(scope="module")
def session_plex(root_dir):
    """
    Fixture to return the prometheus log exporter module.
    """
    # Ensure the parent directory is in the sys.path
    path = root_dir / "birdhouse" / "optional-components" / "prometheus-log-parser" / "config" / "thredds"
    sys.path.append(str(path))
    return importlib.import_module("prometheus-log-exporter")


@pytest.fixture(scope="function")
def plex(session_plex):
    """
    Returns the prometheus log exporter module with an empty counter instance.
    """
    # Clear the counter before each test
    session_plex.counter.clear()
    return session_plex
