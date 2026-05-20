from pathlib import Path
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
    def _(command, expect_error=False, compose=None, unset_env=None, **kwargs):
        # WARNING: DO NOT forward 'os.environ', could break certain test assumptions
        kwargs_env = kwargs.get("env", {})
        kwargs["env"] = {
            "__BIRDHOUSE_SUPPORTED_INTERFACE": "False",
            "BIRDHOUSE_LOCAL_ENV": local_env_file,
            "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False",
            **kwargs_env,
        }
        if compose:
            kwargs["env"]["BIRDHOUSE_COMPOSE"] = compose
        if unset_env:
            for var in unset_env:
                kwargs["env"].pop(var)
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
    assert len(proc.stderr.splitlines()) == 2
    assert not proc.stdout


def test_usage_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} some-arg-that-does-not-go-here", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert len(proc.stderr.splitlines()) == 2
    assert not proc.stdout


def test_usage_some_invalid_arg(cli_path, run):
    proc = run(f"{cli_path} -b some-arg-that-does-not-go-here", expect_error=True)
    assert "USAGE:" in proc.stderr
    assert len(proc.stderr.splitlines()) == 2
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
    assert len(proc.stderr.splitlines()) == 2
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
    assert len(proc.stderr.splitlines()) == 2
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


@pytest.fixture
def config_command_env():
    return {
        "COMPOSE_DIR": "/some/other/path/",
        "BIRDHOUSE_LOG_QUIET": "False",
        "BIRDHOUSE_LOG_DEST_OVERRIDE": ":DEBUG:fd:1",
        "BIRDHOUSE_LOG_FD": "3",
        "BIRDHOUSE_LOG_FILE": "test.log",
        "BIRDHOUSE_LOG_LEVEL": "WARN",
        "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED": "False",
        "BIRDHOUSE_LOCAL_ENV": Path.cwd() / "example.env"
    }


CONFIG_PARAMS=(("--quiet", "", "BIRDHOUSE_LOG_QUIET", "True"),
               ("--quiet", "INFO", "BIRDHOUSE_LOG_DEST_OVERRIDE", ":DEBUG:fd:1:INFO:quiet:", ":INFO:quiet:"),
               ("--log-stdout", "", "BIRDHOUSE_LOG_FD", "1"),
               ("--log-stdout", "INFO", "BIRDHOUSE_LOG_DEST_OVERRIDE", ":DEBUG:fd:1:INFO:fd:1", ":INFO:fd:1"),
               ("--log-file", "test2.log", "BIRDHOUSE_LOG_FILE", Path.cwd() / "test2.log"),
               ("--log-file", "INFO test2.log", "BIRDHOUSE_LOG_DEST_OVERRIDE", f":DEBUG:fd:1:INFO:file:{Path.cwd() / 'test2.log'}", f":INFO:file:{Path.cwd() / 'test2.log'}"),
               ("--log-level", "INFO", "BIRDHOUSE_LOG_LEVEL", "INFO"),
               ("--backwards-compatible", "", "BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED", "True"),
               ("--env-file", Path.cwd() / "example2.env", "BIRDHOUSE_LOCAL_ENV", Path.cwd() / "example2.env"))


@pytest.mark.parametrize("env", ("full", "empty"))
@pytest.mark.parametrize("params", CONFIG_PARAMS, ids=[f"{c[0]}{' <arg>' if c[1] else ''}" for c in CONFIG_PARAMS])
def test_configs_print_config_command(cli_path, run, config_command_env, root_dir, params, env):
    flag, flag_value, env_var, env_value, *empty_values = params
    unset_env = [] if env == "full" else ["BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED", "BIRDHOUSE_LOCAL_ENV"]
    env = config_command_env if env == "full" else {}
    proc = run(f"{cli_path} {flag} {flag_value} configs --print-config-command", unset_env=unset_env, env=env)
    out = [s for line in proc.stdout.split(";") if (s := line.strip())]
    source_i = next(i for i, x in enumerate(out) if x.startswith(". "))
    cmd_i = out.index("read_configs")
    prefix = out[:source_i]
    cmd = out[source_i:cmd_i + 1]
    suffix = out[cmd_i + 1:]
    assert not proc.stderr
    assert "export __BIRDHOUSE_SUPPORTED_INTERFACE=True" in prefix
    assert "unset __BIRDHOUSE_SUPPORTED_INTERFACE" in suffix
    assert f"export COMPOSE_DIR={root_dir / 'birdhouse'}" in prefix
    assert cmd == [f". {root_dir / 'birdhouse' / 'read-configs.include.sh'}", "read_configs"]
    if env:
        assert f"export {env_var}='{env_value}'" in prefix
        assert f"COMPOSE_DIR='{env['COMPOSE_DIR']}'" in suffix
        assert f"{env_var}='{env[env_var]}'" in suffix
    else:
        assert f"export {env_var}='{empty_values[0] if empty_values else env_value}'" in prefix
        assert "COMPOSE_DIR=''" in suffix
        if env_var in unset_env:
            assert f"unset {env_var}" in suffix
        else:
            assert f"{env_var}=''" in suffix


@pytest.mark.parametrize("env", ("full", "empty"))
@pytest.mark.parametrize("params", CONFIG_PARAMS[:-1], ids=[f"{c[0]}{' <arg>' if c[1] else ''}" for c in CONFIG_PARAMS[:-1]])
def test_configs_print_log_command(cli_path, run, config_command_env, root_dir, params, env):
    flag, flag_value, env_var, env_value, *empty_values = params
    unset_env = [] if env == "full" else ["BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED", "BIRDHOUSE_LOCAL_ENV"]
    env = config_command_env if env == "full" else {}
    proc = run(f"{cli_path} {flag} {flag_value} configs --print-log-command", unset_env=unset_env, env=env)
    out = [s for line in proc.stdout.split(";") if (s := line.strip())]
    source_i = next(i for i, x in enumerate(out) if x.startswith(". "))
    prefix = out[:source_i]
    cmd = out[source_i]
    suffix = out[source_i + 1:]
    assert not proc.stderr
    assert not suffix
    assert cmd == f". {root_dir / 'birdhouse' / 'scripts' / 'logging.include.sh'}"
    if env:
        assert f"export {env_var}='{env_value}'" in prefix
    else:
        assert f"export {env_var}='{empty_values[0] if empty_values else env_value}'" in prefix


@pytest.mark.parametrize("flag", ["-s", "--log-stdout"])
def test_log_stdout(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag} compose", compose=logging_script, expect_error=True)
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stdout)


@pytest.mark.parametrize("flag", ["--log-file ", "-l ", "--log-file=", "-l="])
def test_log_file(cli_path, run, flag, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} {flag}{log_path} compose", compose=logging_script, expect_error=True)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stderr)
    assert not proc.stdout


def test_default_log_fd(cli_path, run, logging_script):
    proc = run(f"{cli_path} compose", compose=logging_script, expect_error=True)
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stderr)
    assert not proc.stdout


@pytest.mark.parametrize("flag", ["-q", "--quiet"])
def test_log_quiet(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag} compose", compose=logging_script, expect_error=True)
    assert not proc.stdout


def test_log_file_stdout(cli_path, run, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} -l {log_path} -s compose", compose=logging_script, expect_error=True)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    check_log_output(DEFAULT_LOG_CHECK_LEVELS, proc.stdout)


def test_log_file_quiet(cli_path, run, tmp_path, logging_script):
    log_path = tmp_path / "test.log"
    proc = run(f"{cli_path} -l {log_path} -q compose", compose=logging_script, expect_error=True)
    with open(log_path) as f:
        check_log_output(DEFAULT_LOG_CHECK_LEVELS, f.read())
    assert not proc.stdout


@pytest.mark.parametrize("flag", ["-L ", "--log-level ", "-L=", "--log-level="])
def test_log_level_flags(cli_path, run, logging_script, flag):
    proc = run(f"{cli_path} {flag}DEBUG compose", compose=logging_script, expect_error=True)
    check_log_output(LOG_CHECK_LEVELS, proc.stderr)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_level(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L {level} compose", compose=logging_script, expect_error=True)
    check_log_output(LOG_CHECK_LEVELS[LOG_CHECK_LEVELS.index(level) :], proc.stderr)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_stdout(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L DEBUG -s {level} compose", compose=logging_script, expect_error=True)
    check_log_output([level_ for level_ in LOG_CHECK_LEVELS if level_ != level], proc.stderr)
    check_log_output([level], proc.stdout)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_quiet(cli_path, run, logging_script, level):
    proc = run(f"{cli_path} -L DEBUG -q {level} compose", compose=logging_script, expect_error=True)
    check_log_output([level_ for level_ in LOG_CHECK_LEVELS if level_ != level], proc.stderr)
    check_log_output([], proc.stdout)


@pytest.mark.parametrize("level", LOG_LEVELS)
def test_log_override_file(cli_path, run, logging_script, tmp_path, level):
    log_file = tmp_path / "test.log"
    proc = run(
        f"{cli_path} -L DEBUG -l {level} {log_file} compose",
        compose=logging_script,
        expect_error=True,
    )
    with open(log_file) as f:
        check_log_output([level], f.read())
    check_log_output(LOG_CHECK_LEVELS, proc.stderr)


def test_configs_log_override_multiple(cli_path, run, logging_script, tmp_path):
    log_file = tmp_path / "test.log"
    proc = run(
        f"{cli_path} -L DEBUG -l DEBUG {log_file} -s INFO " f"-q WARN -l ERROR {log_file} -q ERROR compose",
        compose=logging_script,
        expect_error=True,
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
        expect_error=True,
    )
    check_log_output(LOG_LEVELS, proc.stderr)
    with open(log_file) as f:
        check_log_output([level for level in LOG_LEVELS if level != "ERROR"], f.read())
    with open(error_log_file) as f:
        check_log_output(["ERROR"], f.read())


@pytest.mark.parametrize("backup_type", ["create", "restore"])
def test_backup_no_volume_error(cli_path, run, backup_type):
    proc = run(
        f"{cli_path} backup {backup_type} -r stac --no-restic",
        env={"BIRDHOUSE_BACKUP_VOLUME": ""},
        expect_error=True,
    )
    assert proc.returncode != 0
    assert "BIRDHOUSE_BACKUP_VOLUME must be specified" in proc.stderr


@pytest.mark.parametrize("backup_type", ["create", "restore"])
def test_backup_volume_not_dir_warning(cli_path, run, backup_type):
    proc = run(
        f"{cli_path} backup {backup_type} -r stac --no-restic",
        env={"BIRDHOUSE_BACKUP_VOLUME": "tmp"},
        expect_error=True,  # error from stack not running, not from the check itself
    )
    assert proc.returncode != 0  # only because we early-stop, not because of the warning itself
    assert f"Backup {backup_type} detected without an explicit directory path" in proc.stderr
    assert "This command requires that the birdhouse stack be running." in proc.stderr, (
        "Expected the check for running stack to be reached since the warning should not raise an error directly."
    )
