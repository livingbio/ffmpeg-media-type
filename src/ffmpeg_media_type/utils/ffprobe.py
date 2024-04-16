import json
from pathlib import Path

from ..schema import FFProbeInfo
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

    # hotfix animate webp
    if (
        probe_info.streams[0].height == 0
        and probe_info.streams[0].width == 0
        and probe_info.format.format_name == "webp_pipe"
        and is_webp_animated(str(input_url))
    ):
        return ffprobe(hotfix_animate_webp(str(input_url)))

    return probe_info
