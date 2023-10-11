import os
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel

from .utils.ffmpeg import FFProbeInfo, ffprobe, get_ffmpeg, load_cache
from .utils.shell import call


class MediaInfo(BaseModel):
    type: Literal["image", "video", "audio"]

    width: int | None = None
    height: int | None = None
    duration: float | None = None

    format: str | None = None
    size: int | None = None
    suggest_ext: str | None = None


def generate_thumbnail(video_path: str, thumbnail_path: str, time_offset: float = 0) -> str:
    ffmpeg_cmd = get_ffmpeg() + [
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

    call(ffmpeg_cmd)

    return thumbnail_path


def _extract_file_extension(uri: str) -> str:
    parsed_uri = urlparse(uri)
    path = parsed_uri.path
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    return extension[1:].lower()


_KNOWN_CODEC_EXTS = {
    "png_pipe": ["png"],
    "svg_pipe": ["svg"],
    "tiff_pipe": ["tiff", "tif"],
    "bmp_pipe": ["bmp"],
    "gif_pipe": ["gif"],
    "jpeg_pipe": ["jpeg", "jpg"],
    "webp_pipe": ["webp"],
    "mjpeg": ["jpg", "jpeg", "mjpeg"],
}


def _guess_media_info(
    uri: str,
    info: FFProbeInfo,
) -> MediaInfo:
    infos = load_cache()
    current_ext = _extract_file_extension(uri)

    format_name = info.format.format_name
    duration = info.format.duration

    # NOTE: handle ffmpeg's image compatibility
    if format_name == "image2":
        format_name = info.streams[0].codec_name

    # NOTE: detect file extension
    if format_name in _KNOWN_CODEC_EXTS:
        common_exts = _KNOWN_CODEC_EXTS[format_name]
    elif format_name in infos:
        common_exts = infos[format_name].common_exts
    else:
        common_exts = []

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
            duration=duration or 0,
            format=format_name,
            size=info.format.size,
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
                duration=duration or 0,
                format=format_name,
                size=info.format.size,
                suggest_ext=suggest_ext,
            )

    # NOTE: if there is no video stream, the media is audio
    return MediaInfo(
        type="audio",
        width=0,
        height=0,
        duration=duration or 0,
        format=format_name,
        size=info.format.size,
        suggest_ext=suggest_ext,
    )


def detect(uri: str) -> MediaInfo:
    probe_info = ffprobe(uri)
    return _guess_media_info(uri, probe_info)
