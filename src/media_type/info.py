import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Literal

from .utils.ffmpeg import FFProbeInfo, ffprobe_file, load_cache


@dataclass
class MediaInfo:
    type: Literal["image", "video", "audio"]

    width: int | None = None
    height: int | None = None
    duration: float | None = None

    format: str | None = None
    size: int | None = None
    suggest_ext: str | None = None


def generate_thumbnail(video_path: str, time_offset: float = 0) -> str:
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    thumbnail_path = os.path.join(temp_dir, "thumbnail.jpg")  # Temporary thumbnail file path

    ffmpeg_cmd = [
        "ffmpeg",  # FFmpeg command
        "-i",
        video_path,  # Input video path
        "-ss",
        str(time_offset),  # Time offset (seek to the specified position)
        "-vframes",
        "1",  # Number of frames to output
        "-vf",
        "scale=320:-1",  # Thumbnail size (width: 320, height: proportional)
        "-q:v",
        "2",  # Quality (2 - high, 5 - low)
        thumbnail_path,  # Output thumbnail path
    ]

    try:
        subprocess.check_output(ffmpeg_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("Error generating thumbnail:", e.output)
        raise

    return thumbnail_path


def _guess_file_info(
    info: FFProbeInfo,
) -> tuple[Literal["image", "video", "audio"], int, int, float]:
    if not info.format.duration or info.format.format_name == "image2":
        return (
            "image",
            info.streams[0].width or 0,
            info.streams[0].height or 0,
            0,
        )

    for stream in info.streams:
        if stream.codec_type == "video":
            width = stream.width
            height = stream.height

            # gif may have duration
            if info.format.format_name == "gif":
                return "image", width or 0, height or 0, info.format.duration or 0
            else:
                return "video", width or 0, height or 0, info.format.duration or 0

    # Audio
    return "audio", 0, 0, info.format.duration or 0


def detect(uri: str) -> MediaInfo:
    probe_info = ffprobe_file(uri)
    infos = load_cache()

    _type, width, height, duration = _guess_file_info(probe_info)

    if probe_info.format.format_name in infos:
        ext = infos[probe_info.format.format_name].common_exts[0]
    else:
        ext = None

    return MediaInfo(
        type=_type,
        width=width,
        height=height,
        duration=duration,
        format=probe_info.format.format_name,
        size=probe_info.format.size,
        suggest_ext=ext,
    )
