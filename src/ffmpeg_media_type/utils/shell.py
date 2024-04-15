import subprocess
from shlex import join
from tempfile import NamedTemporaryFile

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
        raise FfmpegMediaTypeError(f"command failed: {join(e.cmd)}")

    return r.stdout.decode("utf-8")


def create_temp_filename(suffix: str) -> str:
    """
    Create a temporary file path.

    Returns:
        the path to the temporary file
    """

    if not suffix.startswith("."):
        suffix = f".{suffix}"

    # Create a NamedTemporaryFile
    temp = NamedTemporaryFile(delete=True, suffix=suffix)
    temp_path = temp.name

    # Close and delete the temporary file (it won't actually create it)
    temp.close()

    # At this point, temp_path is a path to a non-existent file
    return temp_path
