import json
import os
import re
import subprocess
import pytest

LOG_LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")


@pytest.fixture
def run(root_dir):
    def _(command, expect_error=False, log_level="INFO", supported_interface=True, **kwargs):
        kwargs["env"] = {
            **kwargs.get("env", os.environ),
            "BIRDHOUSE_LOG_LEVEL": log_level,
            "__BIRDHOUSE_SUPPORTED_INTERFACE": str(supported_interface),
            "TERM": os.getenv("TERM", "linux"),
        }
        command = f". {root_dir / 'birdhouse' / 'scripts' / 'logging.include.sh'}; {command}"
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


@pytest.mark.parametrize("message_level", LOG_LEVELS)
def test_filter_default_info(run, message_level):
    """
    Test that log messages are only shown by default when the log message level is at least INFO.
    """
    proc = run(f"log {message_level} test", log_level="")
    error_msg = f"Log message with level '{message_level}' should{{}} be logged when log level is INFO"
    if LOG_LEVELS.index(message_level) < 1:
        assert not proc.stderr, error_msg.format(" not")
    else:
        assert proc.stderr.strip().endswith("test"), error_msg.format("")


@pytest.mark.parametrize("message_level", LOG_LEVELS)
@pytest.mark.parametrize("log_level", LOG_LEVELS)
def test_filter_by_level(run, message_level, log_level):
    """
    Test that log messages are only shown when the log level is set to the same level of the message or a lower log level.
    """
    proc = run(f"log {message_level} test", log_level=log_level)
    error_msg = f"Log message with level '{message_level}' should{{}} be logged when log level is '{log_level}'"
    if LOG_LEVELS.index(message_level) < LOG_LEVELS.index(log_level):
        assert not proc.stderr, error_msg.format(" not")
    else:
        assert proc.stderr.strip().endswith("test"), error_msg.format("")


@pytest.mark.parametrize("log_level", LOG_LEVELS)
def test_log_colour(run, log_level):
    """
    Test that log messages have coloured prefixes by default
    """
    proc = run(f"log {log_level} test", log_level=log_level)
    assert proc.stderr.startswith("\x1b")
    assert proc.stderr.strip().endswith("test")


@pytest.mark.parametrize("log_level", LOG_LEVELS)
def test_log_no_birdhouse_colour(run, log_level):
    """
    Test that log messages do not have coloured prefixes if BIRDHOUSE_COLOR is not set.
    """
    proc = run(f"log {log_level} test", log_level=log_level, env={"BIRDHOUSE_COLOR": "0"})
    assert re.match(r"[A-Z]+:\s+test\n", proc.stderr)


@pytest.mark.parametrize("log_level", LOG_LEVELS)
def test_log_no_colour(run, log_level):
    """
    Test that log messages do not have coloured prefixes if NO_COLOR is set.
    """
    proc = run(f"log {log_level} test", log_level=log_level, env={"NO_COLOR": "1"})
    assert re.match(r"[A-Z]+:\s+test\n", proc.stderr)


def test_log_to_stdout(run):
    """
    Test that log messages go to stdout when BIRDHOUSE_LOG_FD=1
    """
    proc = run("log INFO test", env={"BIRDHOUSE_LOG_FD": "1"})
    assert proc.stdout.strip().endswith("test")
    assert not proc.stderr


def test_log_quiet(run):
    """
    Test that log messages are suppressed when BIRDHOUSE_LOG_QUIET=True
    """
    proc = run("log INFO test", env={"BIRDHOUSE_LOG_QUIET": "True"})
    assert not proc.stdout
    assert not proc.stderr


def test_log_to_file_and_stderr(run, tmp_path):
    """
    Test that log messages go to a file and stderr when BIRDHOUSE_LOG_FILE is set
    """
    log_file = tmp_path / "test.log"
    proc = run("log INFO test", env={"BIRDHOUSE_LOG_FILE": str(log_file)})
    assert log_file.read_text().strip().endswith("test")
    assert proc.stderr.strip().endswith("test")
    assert not proc.stdout


def test_log_to_file_and_stdout(run, tmp_path):
    """
    Test that log messages go to a file and stdout when BIRDHOUSE_LOG_FILE is set
    and BIRDHOUSE_LOG_FD=1
    """
    log_file = tmp_path / "test.log"
    proc = run("log INFO test", env={"BIRDHOUSE_LOG_FILE": str(log_file), "BIRDHOUSE_LOG_FD": "1"})
    assert log_file.read_text().strip().endswith("test")
    assert proc.stdout.strip().endswith("test")
    assert not proc.stderr


def test_log_to_file_and_quiet(run, tmp_path):
    """
    Test that log messages go only to a file when BIRDHOUSE_LOG_FILE is set
    and BIRDHOUSE_LOG_QUIET=True
    """
    log_file = tmp_path / "test.log"
    proc = run("log INFO test", env={"BIRDHOUSE_LOG_FILE": str(log_file), "BIRDHOUSE_LOG_QUIET": "True"})
    assert log_file.read_text().strip().endswith("test")
    assert not proc.stdout
    assert not proc.stderr


def test_invalid_log_message_level(run):
    """
    Test that setting an invalid log message level will write to CRITICAL and exit with an error
    """
    proc = run("log BADBADLEVEL test", expect_error=True)
    assert "CRITICAL" in proc.stderr
    assert "Invalid log level" in proc.stderr
    assert proc.returncode == 2


def test_invalid_critical_log_message_level(run):
    """
    Test that CRITICAL is treated as an invalid log level.
    """
    proc = run("log CRITICAL test", expect_error=True)
    assert "CRITICAL" in proc.stderr
    assert "Invalid log level" in proc.stderr
    assert proc.returncode == 2


def test_empty_log_message(run):
    """
    Test that writing and empty log message will write to CRITICAL and exit with an error
    """
    proc = run("log INFO", expect_error=True)
    assert "CRITICAL" in proc.stderr
    assert "log message is missing" in proc.stderr
    assert proc.returncode == 2


def test_invalid_log_level(run):
    """
    Test that setting an invalid log level will write to CRITICAL and exit with an error
    """
    proc = run("log INFO test", log_level="BADLEVEL", expect_error=True)
    assert "CRITICAL" in proc.stderr
    assert "Invalid log level" in proc.stderr
    assert proc.returncode == 2


@pytest.mark.parametrize("level", LOG_LEVELS)
@pytest.mark.parametrize("dest", ["fd:1", "fd:2", "file:", "quiet:"])
@pytest.mark.parametrize(
    "default_dest",
    [
        '{"BIRDHOUSE_LOG_FD": "1"}',
        '{"BIRDHOUSE_LOG_FD": "2"}',
        '{"BIRDHOUSE_LOG_QUIET": "True"}',
        '{"BIRDHOUSE_LOG_FILE": ""}',
    ],
)
def test_log_dest_override(run, tmp_path, level, dest, default_dest):
    """
    Test that the BIRDHOUSE_LOG_DEST_OVERRIDE command works as expected when combined with various other log settings

    Rules in order of precedence:

    - 'quiet:' or BIRDHOUSE_LOG_QUIET=True prevents writing to a file descriptor
    - 'fd:1' or 'fd:2' writes to the specified file descriptor
    - 'file:<name>' writes to the specified file <name> instead of BIRDHOUSE_LOG_FILE
    """
    log_file = tmp_path / "test.log"
    default_log_file = tmp_path / "default.log"
    default_dest = json.loads(default_dest)  # load from json so that test name contains readable info about the test
    if dest.startswith("file:"):
        dest += str(log_file)
    if "BIRDHOUSE_LOG_FILE" in default_dest:
        default_dest["BIRDHOUSE_LOG_FILE"] = str(default_log_file)
    proc = run(
        f"log {level} test", log_level=level, env={**default_dest, "BIRDHOUSE_LOG_DEST_OVERRIDE": f"{level}:{dest}"}
    )
    if dest == "quiet:" or dest.startswith("fd:") and "BIRDHOUSE_LOG_QUIET" in default_dest:
        assert not proc.stderr
        assert not proc.stdout
    elif dest == "fd:1":
        assert proc.stdout.strip().endswith("test")
    elif dest == "fd:2":
        assert proc.stderr.strip().endswith("test")
    else:
        assert log_file.read_text().strip().endswith("test")
    if "BIRDHOUSE_LOG_FILE" in default_dest and not dest.startswith("file:"):
        assert default_log_file.read_text().strip().endswith("test")


def test_write_multiline(run):
    """
    Test that logging multiline strings is supported
    """
    proc = run("log INFO 'test\ntest2'")
    assert proc.stderr.strip().endswith("test\n          test2")  # second line is indented 10 spaces


def test_write_multiline_keep_spacing(run):
    """
    Test that spacing is preserved when logging multiline strings
    """
    proc = run("log INFO 'test\n  test2'")
    assert proc.stderr.strip().endswith("test\n            test2")  # second line is indented 12 (10+2) spaces
