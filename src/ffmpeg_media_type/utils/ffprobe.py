import json

from ..schema import FFProbeInfo
from .loader import from_dict
from .shell import call


def ffprobe(input_url: str) -> FFProbeInfo:

    # Construct the FFprobe command with JSON output format
    ffprobe_cmd = ["ffprobe"] + [
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        input_url,
    ]

    # Execute the FFprobe command and capture the output
    output = call(ffprobe_cmd)
    return from_dict(FFProbeInfo, json.loads(output))