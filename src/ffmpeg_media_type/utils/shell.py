import subprocess

from ..exceptions import FfmpegMediaTypeError


def call(cmds: list[str]) -> str:
    """
    Run a command and return the stdout.

    Args:
        cmds: List of command and arguments.

    Raises:
        FfmpegMediaTypeError: If the command fails.

    Returns:
        stdout of the command.
    """
    try:
        r = subprocess.run(cmds, stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise FfmpegMediaTypeError(f"command failed: {e.cmd}")

    return r.stdout.decode("utf-8")
