import json
import subprocess
from functools import lru_cache
from pathlib import Path
from urllib.request import urlretrieve

from ..schema import FFProbeInfo
from .loader import from_dict
from .shell import call, create_temp_filename


def _is_url(uri: str | Path) -> bool:
    """
    Check if the URI is a URL.

    Args:
        uri: The URI to check.

    Returns:
        True if the URI is a URL, False otherwise.
    """
    return isinstance(uri, str) and uri.startswith(("http://", "https://"))


def _ensure_downloaded(uri: str) -> str:
    """
    Download a file from a URL.

    Args:
        uri: The URL of the file to download.

    Returns:
        The path to the downloaded file.
    """
    if not _is_url(uri):
        return uri

    # Download the file
    file_path = create_temp_filename(".webp")
    urlretrieve(uri, file_path)

    return file_path


@lru_cache()
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


def is_webp_animated(file_path: str) -> bool:
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
    result = subprocess.run(["webpmux", "-info", file_path], capture_output=True, text=True)
    output = result.stdout

    # Check output for the presence of 'ANMF' chunk which indicates animation
    if "Number of frames" in output:
        return True
    else:
        return False


def extract_animated_webp_frame(uri: str) -> str:
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
    temp_uri = create_temp_filename(".webp")
    webpmux_command = ["webpmux", "-get", "frame", "1", uri, "-o", temp_uri]
    call(webpmux_command)
    return temp_uri


def is_webp_need_fix(uri: str | Path) -> bool:
    """
    Check if a WebP file needs to be fixed.

    Args:
        uri: The URI of the WebP file.

    Returns:
        True if the WebP file is animated, False otherwise.

    Raises:
        FfmpegMediaTypeError: If the ffprobe command fails.
    """

    ffprobe_cmd = ["ffprobe"] + [
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(uri),
    ]

    # Execute the FFprobe command and capture the output
    output = call(ffprobe_cmd)
    probe_info = from_dict(FFProbeInfo, json.loads(output))

    if probe_info.format.format_name != "webp_pipe":
        return False

    if probe_info.streams[0].height == 0 and probe_info.streams[0].width == 0:
        return True

    return False


def hotfix_animate_webp(uri: str | Path) -> str:
    """
    Fix a WebP file if it is animated.

    Args:
        uri: The URI of the WebP file.

    Returns:
        The URI of the fixed WebP file if it was animated, otherwise the original URI.

    Raises:
        FfmpegMediaTypeError: If the webpmux command fails.

    Notes:
        Some WebP files (e.g. animated WebP files) may not be supported by ffmpeg.
        This function can be used to fix such files by extracting the first frame.
        If webpmux is not installed, the original URI will be returned.
    """

    if check_webpmux_installed() is None:
        # webpmux is not installed, so we cannot fix the WebP file
        return str(uri)

    if not is_webp_need_fix(str(uri)):
        # The WebP file work with ffprobe, so no fix is needed
        return str(uri)

    downloaded_file = _ensure_downloaded(str(uri))
    if not is_webp_animated(downloaded_file):
        # The WebP file is not animated, so no fix is needed
        return str(uri)

    # The WebP file is animated, so extract the first frame
    return extract_animated_webp_frame(downloaded_file)
