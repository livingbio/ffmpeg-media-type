import os
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from .exceptions import FfmpegMediaTypeError
from .schema import FFMpegSupport, MediaInfo
from .utils.cache import load
from .utils.ffprobe import ffprobe
from .utils.shell import call


def create_temp_file_path(suffix: str) -> str:
    """
    Create a temporary file path.

    Returns:
        the path to the temporary file
    """

    # Create a NamedTemporaryFile
    temp = NamedTemporaryFile(delete=True, suffix=suffix)
    temp_path = temp.name

    # Close and delete the temporary file (it won't actually create it)
    temp.close()

    # At this point, temp_path is a path to a non-existent file
    return temp_path


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


def extract_file_extension_from_uri(uri: str) -> str:
    """
    Extract the file extension from a URI.

    Args:
        uri: the URI to extract the file extension from

    Returns:
        the file extension
    """

    parsed_uri = urlparse(uri)
    path = parsed_uri.path
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    return extension[1:].lower()


KNOWN_CODEC_EXTS = {
    "png_pipe": ("png",),
    "svg_pipe": ("svg",),
    "tiff_pipe": ("tiff", "tif"),
    "bmp_pipe": ("bmp",),
    "gif_pipe": ("gif",),
    "jpeg_pipe": ("jpeg", "jpg"),
    "webp_pipe": ("webp",),
    "mjpeg": ("jpg", "jpeg", "mjpeg"),
}
"""
Dictionary mapping codec names to common file extensions.
"""


def detect(uri: str) -> MediaInfo:
    """
    Detect the media type of a file.

    Args:
        uri: the URI of the file

    Returns:
        the media type information

    Raises:
        FfmpegMediaTypeError: If the ffmpeg command fails.
    """
    info = ffprobe(uri)
    current_ext = extract_file_extension_from_uri(uri)

    format_name = info.format.format_name
    duration = info.format.duration

    # NOTE: handle ffmpeg's image compatibility
    if format_name == "image2":
        format_name = info.streams[0].codec_name

    # NOTE: detect file extension
    if format_name in KNOWN_CODEC_EXTS:
        common_exts = KNOWN_CODEC_EXTS[format_name]
    elif support_info := load(FFMpegSupport, format_name):
        common_exts = support_info.common_exts
    else:
        common_exts = ()

    if current_ext in common_exts:
        suggest_ext = current_ext
    elif common_exts:
        suggest_ext = common_exts[0]
    else:
        suggest_ext = None

    # NOTE: we classify gif as image
    if not duration or format_name in ("gif", "mjpeg"):
        return MediaInfo(
            type="image",
            width=info.streams[0].width or 0,
            height=info.streams[0].height or 0,
            duration=float(duration) if duration is not None else None,
            format=format_name,
            size=int(info.format.size) if info.format.size is not None else None,
            suggest_ext=suggest_ext,
        )

    for stream in info.streams:
        # NOTE: if there is at least one video stream, the media is video
        if stream.codec_type == "video" and format_name not in ("mp3",):
            width = stream.width
            height = stream.height

            return MediaInfo(
                type="video",
                width=width or 0,
                height=height or 0,
                duration=float(duration) if duration is not None else None,
                format=format_name,
                size=int(info.format.size) if info.format.size is not None else None,
                suggest_ext=suggest_ext,
            )

    # NOTE: if there is no video stream, the media is audio
    return MediaInfo(
        type="audio",
        width=0,
        height=0,
        duration=float(duration) if duration is not None else None,
        format=format_name,
        size=int(info.format.size) if info.format.size is not None else None,
        suggest_ext=suggest_ext,
    )
