import pytest


@pytest.fixture(scope="module")
def root_dir(request):
    # implement this for every testing subfolder
    yield request.path.parent.parent.parent


@pytest.fixture(scope="module")
def local_env_file(root_dir):
    yield root_dir / "tests" / "test.env"


@pytest.fixture(scope="session")
def session_plex():
    """
    Fixture to return the prometheus log exporter module.
    """
    import sys
    from pathlib import Path
    import importlib.util

    # Ensure the parent directory is in the sys.path
    root = Path(__file__).parent.parent.parent
    path = root  / "birdhouse" / "optional-components" / "prometheus-log-parser" / "config" / "thredds"
    spec = importlib.util.spec_from_file_location("prometheus_log_exporter", str(path / "prometheus-log-exporter.py"))
    plex = importlib.util.module_from_spec(spec)
    sys.modules["prometheus_log_exporter"] = plex
    spec.loader.exec_module(plex)
    return plex


@pytest.fixture(scope="function")
def plex(session_plex):
    """
    Fixture to return a fresh instance of the prometheus log exporter module for each test.
    """
    # Clear the counter before each test
    session_plex.counter.clear()
    return session_plex
