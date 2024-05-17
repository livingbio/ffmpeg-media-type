from pathlib import Path

from .hotfix_webp import hotfix_animate_webp
from .shell import call, create_temp_filename


def generate_thumbnail(
    video_path: str | Path, suffix: str = ".png", *, width: int = 320, height: int = -1, time_offset: float = 0
) -> str:
    """
    Generate a thumbnail from a video file at a specified time offset.

    Args:
        video_path: the path to the video file
        suffix: the suffix of the generated thumbnail
        width: the width of the generated thumbnail
        height: the height of the generated thumbnail
        time_offset: the time offset in seconds to generate the thumbnail

    Raises:
        FfmpegMediaTypeError: If the ffmpeg command fails.

    Returns:
        the path to the generated thumbnail
    """

    video_path = hotfix_animate_webp(video_path)

    thumbnail_path = create_temp_filename(suffix)
    ffmpeg_cmd = ["ffmpeg"] + [
        "-y",  # Overwrite output file if it exists
        "-i",
        str(video_path),  # Input video path
        "-ss",
        str(time_offset),  # Time offset (seek to the specified position)
        "-vframes",
        "1",  # Number of frames to output
        "-vf",
        f"scale={width}:{height}",  # Thumbnail size (width: 320, height: proportional)
        "-q:v",
        "2",  # Quality (2 - high, 5 - low)
        thumbnail_path,  # Output thumbnail path
    ]

    call(ffmpeg_cmd)

    return thumbnail_path
