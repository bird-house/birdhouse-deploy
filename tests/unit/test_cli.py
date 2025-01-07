import os
import subprocess

import pytest


TEST_LOG_ID_STRING = "test logging {}"

LOG_LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]

LOG_CHECK_LEVELS = LOG_LEVELS + ["CRITICAL"]

DEFAULT_LOG_CHECK_LEVELS = LOG_CHECK_LEVELS[1:]


@pytest.fixture(scope="module")
def cli_path(root_dir):
    yield root_dir / "bin" / "birdhouse"


@pytest.fixture(scope="module")
def echo_args_script(root_dir):
    yield root_dir / "tests" / "fixtures" / "echo_args.sh"


@pytest.fixture(scope="module")
def printenv_script(root_dir):
    yield root_dir / "tests" / "fixtures" / "printenv.sh"


@pytest.fixture(scope="module")
def logging_script(root_dir):
    yield root_dir / "tests" / "fixtures" / "log_examples.sh"


@pytest.fixture
def run(local_env_file):
    def _(command, expect_error=False, compose=None, **kwargs):
        kwargs["env"] = {
            **kwargs.get("env", os.environ),
            "BIRDHOUSE_LOCAL_ENV": local_env_file,
        }
        if compose:
            kwargs["env"]["BIRDHOUSE_COMPOSE"] = compose
        proc = subprocess.run(
            str(command),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            **kwargs,
        )
        if proc.returncode and not expect_error:
            raise subprocess.SubprocessError(
                f"'{command}' failed with return code: {proc.returncode}\nError:\n{proc.stderr}"
            )
        return proc

    return _


def check_log_output(levels, log_content):
    for log_level in LOG_LEVELS:
        log_string = TEST_LOG_ID_STRING.format(log_level.lower())
        if log_level in levels:
            assert log_string in log_content
        else:
            assert log_string not in log_content
    if "CRITICAL" in levels:
        last_line = log_content.splitlines()[-1]
        assert "CRITICAL" in last_line
        assert "Invalid log level" in last_line


def test_help(cli_path, run):
    proc = run(f"{cli_path} --help")
    assert "USAGE:" in proc.stdout
    assert len(proc.stdout.splitlines()) > 1
    assert not proc.stderr


def test_help_with_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} --help some-arg-that-does-not-go-here")
    assert "USAGE:" in proc.stdout
    assert len(proc.stdout.splitlines()) > 1
    assert not proc.stderr


def test_usage_no_args(cli_path, run):
    proc = run(cli_path, expect_error=True)
    assert "USAGE:" in proc.stderr
    assert len(proc.stderr.splitlines()) == 1
    assert not proc.stdout


def test_usage_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} some-arg-that-does-not-go-here", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert len(proc.stderr.splitlines()) == 1
    assert not proc.stdout


def test_usage_some_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} -b some-arg-that-does-not-go-here", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert len(proc.stderr.splitlines()) == 1
    assert not proc.stdout


def test_info(cli_path, run, echo_args_script):
    proc = run(f"{cli_path} info", compose=echo_args_script)
    assert proc.stdout.strip() == "CALLED_WITH_ARGS: info"


def test_compose(cli_path, run, echo_args_script):
    proc = run(f"{cli_path} compose some compose command", compose=echo_args_script)
    assert proc.stdout.strip() == "CALLED_WITH_ARGS: some compose command"


@pytest.mark.parametrize("flag", ["--backwards-compatible", "-b"])
def test_compose_backwards_compatible(cli_path, run, printenv_script, flag):
    proc = run(f"{cli_path} {flag} compose", compose=printenv_script)
    assert "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED=True" in proc.stdout.splitlines()


@pytest.mark.parametrize("flag", ["--env-file ", "-e ", "--env-file=", "-e="])
def test_compose_set_env_file(cli_path, run, printenv_script, local_env_file, tmp_path, flag):
    other_local_env_file = tmp_path / "env.local.other"
    with open(local_env_file) as f:
        other_local_env_file.write_text(f.read())
    proc = run(
        f"{cli_path} {flag}{other_local_env_file} compose",
        compose=printenv_script,
    )
    assert f"BIRDHOUSE_LOCAL_ENV={other_local_env_file}" in proc.stdout.splitlines()


def test_configs_no_args(cli_path, run):
    proc = run(f"{cli_path} configs", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert "configs" in proc.stderr
    assert len(proc.stderr.splitlines()) == 1
    assert not proc.stdout


def test_configs_help(cli_path, run):
    proc = run(f"{cli_path} configs --help")
    assert "USAGE:" in proc.stdout
    assert "configs" in proc.stdout
    assert len(proc.stdout.splitlines()) > 1
    assert not proc.stderr


def test_configs_invalid_args(cli_path, run):
    proc = run(f"{cli_path} configs some-arg-that-does-not-go-here", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert "configs" in proc.stderr
    assert len(proc.stderr.splitlines()) == 1
    assert not proc.stdout


def test_configs_help_with_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} configs --help some-arg-that-does-not-go-here")
    assert "USAGE:" in proc.stdout
    assert "configs" in proc.stdout
    assert len(proc.stdout.splitlines()) > 1
    assert not proc.stderr


@pytest.mark.parametrize("flag", ["--env-file ", "-e ", "--env-file=", "-e="])
def test_configs_set_env_file(cli_path, run, local_env_file, tmp_path, flag):
    other_local_env_file = tmp_path / "env.local.other"
    with open(local_env_file) as f:
        other_local_env_file.write_text(f.read())
    proc = run(f"{cli_path} {flag}{other_local_env_file} configs -p")
    assert f"BIRDHOUSE_LOCAL_ENV='{other_local_env_file}'" in proc.stdout
    assert f"BIRDHOUSE_LOCAL_ENV='{local_env_file}'" in proc.stdout.split(str(other_local_env_file))[-1]


@pytest.mark.parametrize("flag", ["-s", "--log-stdout"])
def test_log_stdout(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag} compose", compose=logging_script)
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stdout)
    assert not proc.stderr


@pytest.mark.parametrize("flag", ["--log-file ", "-l ", "--log-file=", "-l="])
def test_log_file(cli_path, run, flag, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} {flag}{log_path} compose", compose=logging_script)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stderr)
    assert not proc.stdout


def test_default_log_fd(cli_path, run, logging_script):
    proc = run(f"{cli_path} compose", compose=logging_script)
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stderr)
    assert not proc.stdout


@pytest.mark.parametrize("flag", ["-q", "--quiet"])
def test_log_quiet(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag} compose", compose=logging_script)
    assert not proc.stdout
    assert not proc.stderr


def test_log_file_stdout(cli_path, run, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} -l {log_path} -s compose", compose=logging_script)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stdout)
    assert not proc.stderr


def test_log_file_quiet(cli_path, run, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} -l {log_path} -q compose", compose=logging_script)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    assert not proc.stdout
    assert not proc.stderr


@pytest.mark.parametrize("flag", ["-L ", "--log-level ", "-L=", "--log-level="])
def test_log_level_flags(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag}DEBUG compose", compose=logging_script)
    check_log_output(LOG_CHECK_LEVELS, proc.stderr)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_level(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L {level} compose", compose=logging_script)
    check_log_output(LOG_CHECK_LEVELS[LOG_CHECK_LEVELS.index(level) :], proc.stderr)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_stdout(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L DEBUG -s {level} compose", compose=logging_script)
    check_log_output([level_ for level_ in LOG_CHECK_LEVELS if level_ != level], proc.stderr)
    check_log_output([level], proc.stdout)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_quiet(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L DEBUG -q {level} compose", compose=logging_script)
    check_log_output([level_ for level_ in LOG_CHECK_LEVELS if level_ != level], proc.stderr)
    check_log_output([], proc.stdout)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_file(cli_path, run, logging_script, tmp_path, level):
    log_file = tmp_path / "test.log"
    proc = run(
        f"{cli_path} -L DEBUG -l {level} {log_file} compose",
        compose=logging_script,
    )
    with open(log_file) as f:
        check_log_output([level], f.read())
    check_log_output(LOG_CHECK_LEVELS, proc.stderr)


def test_configs_log_override_multiple(cli_path, run, logging_script, tmp_path):
    log_file = tmp_path / "test.log"
    proc = run(
        f"{cli_path} -L DEBUG -l DEBUG {log_file} -s INFO " f"-q WARN -l ERROR {log_file} -q ERROR compose",
        compose=logging_script,
    )
    check_log_output(["DEBUG"], proc.stderr)
    check_log_output(["INFO"], proc.stdout)
    with open(log_file) as f:
        check_log_output(["DEBUG", "ERROR"], f.read())


def test_configs_log_override_file_default(cli_path, run, logging_script, tmp_path):
    log_file = tmp_path / "test.log"
    error_log_file = tmp_path / "test-error.log"
    proc = run(
        f"{cli_path} -L DEBUG -l {log_file} -l ERROR {error_log_file} compose",
        compose=logging_script,
    )
    check_log_output(LOG_LEVELS, proc.stderr)
    with open(log_file) as f:
        check_log_output([level for level in LOG_LEVELS if level != "ERROR"], f.read())
    with open(error_log_file) as f:
        check_log_output(["ERROR"], f.read())
