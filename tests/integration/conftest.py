import json
import os
import shutil
import subprocess
import sys
import time
import pytest


@pytest.fixture(scope="module")
def root_dir(request):
    yield request.path.parent.parent.parent


@pytest.fixture(scope="module")
def cli_path(root_dir):
    yield root_dir / "bin" / "birdhouse"


@pytest.fixture(scope="session", autouse=True)
def check_stack_not_running(request):
    """
    Check that the stack isn't already running before starting the tests.
    """
    if request.config.getoption("--no-start-stack", None):
        return
    proc = subprocess.run(
        "docker ps --filter label=com.docker.compose.project --format 'table {{.Label \"com.docker.compose.project\"}}'",
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if proc.returncode:
        pytest.fail("Docker may not be running. This test cannot run without docker.")

    test_project_name = os.getenv("TEST_COMPOSE_PROJECT_NAME", "birdhouse-test-stack")
    project_name = os.getenv("COMPOSE_PROJECT_NAME", "birdhouse")
    lines = proc.stdout.splitlines()
    if test_project_name in lines or project_name in lines:
        pytest.fail(
            "Birdhouse is currently running. Please stop the software before running tests."
        )


@pytest.fixture(scope="session")
def tmp_data_persist_root(tmp_path_factory):
    yield tmp_path_factory.mktemp("data-persist-root")


@pytest.fixture(scope="session")
def stack_info():
    """
    Used to store information about the birhouse stack start-up so that it
    isn't started multiple times per session.
    """
    info = {"started": False}
    yield info


@pytest.fixture(scope="module", autouse=True)
def load_stack_env(cli_path, local_env_file, stack_info):
    if stack_info["started"]:
        return
    proc = subprocess.run(
        f"{cli_path} -e {local_env_file} configs -c 'env -0'",
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if proc.returncode:
        pytest.fail(f"Unable to get environment variables. Error:\n{proc.stderr}")
    env_vars = dict(
        line.split("=", 1) for line in proc.stdout.split("\x00") if "=" in line
    )
    print(env_vars["MAGPIE_ADMIN_USERNAME"])
    stack_info["env_vars"] = env_vars


@pytest.fixture(scope="module")
def stack_env(stack_info):
    return stack_info["env_vars"]


@pytest.fixture(scope="module")
def birdhouse_url(stack_env):
    return (
        f"{stack_env['BIRDHOUSE_PROXY_SCHEME']}://{stack_env['BIRDHOUSE_FQDN_PUBLIC']}"
    )


@pytest.fixture(scope="module", autouse=True)
def start_stack(
    request, cli_path, local_env_file, tmp_data_persist_root, stack_info, pytestconfig
):
    """
    Starts the birdhouse stack at the beginning of the test session.

    This is module scoped because it relies on other module scoped fixtures. However,
    it will actually only be fully run once per session.
    """
    stack_info["local_env_file"] = local_env_file
    stack_info["data_persist_root"] = tmp_data_persist_root
    stack_info["cli_path"] = cli_path
    if request.config.getoption("--no-start-stack", None) or stack_info["started"]:
        stack_info["started"] = True
        return
    env = {
        "TEST_BIRDHOUSE_DATA_PERSIST_ROOT": tmp_data_persist_root / "data",
        "TEST_BIRDHOUSE_LOG_DIR": tmp_data_persist_root / "logs",
        **os.environ,
    }
    if request.session.config.getoption("-m").strip() == "minimal":
        env["TEST_BIRDHOUSE_EXTRA_CONF_DIRS"] = " "
    stack_info["started"] = True
    flags = "-s" if pytestconfig.option.capture == "no" else ""
    proc = subprocess.run(
        f"{cli_path} {flags} -e {local_env_file} compose up -d",
        shell=True,
        stderr=subprocess.PIPE,
        env=env,
        universal_newlines=True,
    )
    if proc.returncode:
        pytest.fail(f"Unable to start the Birdhouse stack. Error:\n{proc.stderr}")

    timeout = int(request.config.getoption("--wait-for-healthy-timeout", 60))
    start = time.time()
    project_name = os.getenv("TEST_COMPOSE_PROJECT_NAME", "birdhouse-test-stack")
    containers_proc = subprocess.run(
        f"docker ps --filter label=com.docker.compose.project={project_name} -aq --no-trunc",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if proc.returncode:
        pytest.fail(proc.stderr)
    while start + timeout > time.time():
        proc = subprocess.run(
            'docker inspect --format \'{{if .State.Health}}{"health": {{json .State.Health.Status}}, '
            '"name": {{json .Name}}}{{end}}\' '
            + containers_proc.stdout.replace("\n", " "),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        if proc.returncode:
            pytest.fail(proc.stderr)
        health_stats = []
        for status in proc.stdout.splitlines():
            if status.strip():
                status = json.loads(status)
                if status["health"] != "healthy":
                    health_stats.append(
                        f"name: '{status['name'].strip().strip('/')}', status: '{status['health']}'"
                    )
        if any(health_stats):
            msg = "Waiting on the following containers to be healthy:\n" + "\n".join(
                health_stats
            )
            print(msg, file=sys.stderr)
        else:
            break
        time.sleep(min(timeout // 10, 5))
    else:
        pytest.fail(
            f"Birdhouse stack is not healthy after waiting {timeout} seconds timeout. Current status:\n {proc.stdout}"
        )


@pytest.fixture(scope="session", autouse=True)
def stop_stack(request, stack_info, pytestconfig):
    """
    Stops the stack at the end of the test session.
    """
    yield
    flags = "-s" if pytestconfig.option.capture == "no" else ""
    if stack_info["started"] and not request.config.getoption("--no-stop-stack", None):
        proc = subprocess.run(
            f"{stack_info['cli_path']} {flags} -e '{stack_info['local_env_file']}' "
            "compose down -v --remove-orphans",
            shell=True,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        if proc.returncode:
            pytest.exit(
                f"Unable to stop the Birdhouse stack. Error:\n\n {proc.stderr}",
                returncode=1,
            )
        if not request.config.getoption("--no-rm-data", None):
            shutil.rmtree(stack_info["data_persist_root"])
