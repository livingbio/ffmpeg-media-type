import subprocess
from pathlib import Path

from .shell import call, create_temp_filename


def check_webpmux_installed() -> str | None:
    """
    Check if webpmux is installed.

    Returns:
        The version info of webpmux if it is installed, otherwise None.
    """

    try:
        # Attempt to run `webpmux -version` to check if webpmux is installed
        result = subprocess.run(["webpmux", "-version"], capture_output=True, text=True, check=True)
        # print("webpmux is installed. Version info:")
        # print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # The command was found, but it exited with an error
        # print("webpmux command failed:", e)
        return None
    except FileNotFoundError:
        # The command was not found
        # print("webpmux is not installed.")
        return None


def is_webp_animated(file_path: str | Path) -> bool:
    """
    Check if a WebP file is animated.

    Args:
        file_path: The path to the WebP file.

    Returns:
        True if the WebP file is animated, False otherwise.

    Raises:
        FfmpegMediaTypeError: If the webpmux command fails.
    """

    # Running the webpmux command to get information about the WebP file
    result = subprocess.run(["webpmux", "-info", str(file_path)], capture_output=True, text=True)
    output = result.stdout

    # Check output for the presence of 'ANMF' chunk which indicates animation
    if "Number of frames" in output:
        return True
    else:
        return False


def extract_animated_webp_frame(uri: str | Path) -> str:
    """
    Fix an animated webp file by extracting the first frame.

    Args:
        uri: The URI of the webp file.

    Returns:
        The URI of the fixed webp file.

    Raises:
        FfmpegMediaTypeError: If the webpmux command fails.

    Notes:
        Will raise Exception if the webp file is not animated.
    """
    # HOTFIX: some webp files are not correctly handled by ffmpeg
    temp_uri = create_temp_filename(".webp")
    webpmux_command = ["webpmux", "-get", "frame", "1", str(uri), "-o", temp_uri]
    call(webpmux_command)
    return temp_uri
