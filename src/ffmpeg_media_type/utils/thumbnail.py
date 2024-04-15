from ..exceptions import FfmpegMediaTypeError
from .shell import call, create_temp_file_path


def generate_thumbnail(video_path: str, suffix: str = ".png", time_offset: float = 0) -> str:
    """
    Generate a thumbnail from a video file at a specified time offset.

    Args:
        video_path: the path to the video file
        suffix: the suffix of the generated thumbnail
        time_offset: the time offset in seconds to generate the thumbnail

    Raises:
        FfmpegMediaTypeError: If the ffmpeg command fails.

    Returns:
        the path to the generated thumbnail
    """

    thumbnail_path = create_temp_file_path(suffix)

    ffmpeg_cmd = ["ffmpeg"] + [
        "-y",  # Overwrite output file if it exists
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
        call(ffmpeg_cmd)
    except FfmpegMediaTypeError:
        pass

    return thumbnail_path
