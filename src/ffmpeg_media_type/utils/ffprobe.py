import json
from pathlib import Path

from ..schema import FFProbeInfo
from .hotfix_webp import hotfix_animate_webp
from .loader import from_dict
from .shell import call


def ffprobe(input_url: str | Path) -> FFProbeInfo:
    """
    Get media information using FFprobe.

    Args:
        input_url: the URI of the media file

    Returns:
        the media information

    Raises:
        FfmpegMediaTypeError: If the FFprobe command fails.
    """

    input_url = hotfix_animate_webp(input_url)

    # Construct the FFprobe command with JSON output format
    ffprobe_cmd = ["ffprobe"] + [
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(input_url),
    ]

    # Execute the FFprobe command and capture the output
    output = call(ffprobe_cmd)
    probe_info = from_dict(FFProbeInfo, json.loads(output))

    return probe_info
