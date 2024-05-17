from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True, kw_only=True)
class FFMpegSupport:
    """
    FFMpeg support info for a codec.
    """

    demuxing_support: bool
    """
    Is ffmpeg support demuxing for the codec.
    """
    muxing_support: bool
    """
    Is ffmpeg support muxing for the codec.
    """
    codec: str
    """
    Codec name.
    """
    description: str
    """
    Codec description.
    """

    common_exts: tuple[str, ...]
    """
    Common file extensions for the codec.
    """
    mime_type: str
    """
    Mime type for the codec.
    """
    default_video_codec: str
    """
    Default video codec for the codec.
    """
    default_audio_codec: str
    """
    Default audio codec for the codec.
    """


@dataclass(frozen=True, kw_only=True)
class MediaInfo:
    """
    The Basic Media info.
    """

    type: Literal["image", "video", "audio"]
    """
    The media type.
    """

    width: int = 0
    """
    The media width.
    """
    height: int = 0
    """
    The media height.
    """
    duration: float = 0
    """
    The media duration.
    """

    format: str | None = None
    """
    The media format.
    """
    size: int = 0
    """
    The media size.
    """
    suggest_ext: str | None = None
    """
    The suggested file extension.
    """


@dataclass(kw_only=True, frozen=True)
class FFProbeFormat:
    """
    The media format info return by ffprobe.
    """

    filename: str | None = None
    """
    The media filename.
    """
    duration: str | None = None
    """
    The media duration.
    """
    format_name: str
    """
    The media format name.
    """
    format_long_name: str | None = None
    """
    The media format long name.
    """
    start_time: float | None = None
    """
    The media start time.
    """
    size: str | None = None
    """
    The media size.
    """
    probe_score: int | None = None
    """
    The media probe score.
    """


@dataclass(kw_only=True, frozen=True)
class FFProbeStreamTags:
    """
    The media stream tags return by ffprobe.
    """

    rotate: int = 0
    """
    The stream rotate value.
    """


@dataclass(kw_only=True, frozen=True)
class FFProbeStream:
    """
    The media stream info return by ffprobe.
    """

    index: int | None = None
    """
    The stream index.
    """
    width: int | None = None
    """
    The stream width.
    """
    height: int | None = None
    """
    The stream height.
    """
    codec_type: str | None = None
    """
    The stream codec type.
    """
    codec_name: str
    """
    The stream codec name.
    """
    codec_long_name: str | None = None
    """
    The stream codec long name.
    """
    profile: str | None = None
    """
    The stream profile.
    """
    pix_fmt: str | None = None
    """
    The stream pixel format.
    """
    r_frame_rate: str | None = None
    """
    The stream frame rate.
    """
    tags: FFProbeStreamTags = field(default_factory=FFProbeStreamTags)
    """
    The stream tags.
    """


@dataclass(kw_only=True, frozen=True)
class FFProbeInfo:
    """
    The media information return by ffprobe.
    """

    format: FFProbeFormat
    """
    The media format info.
    """
    streams: tuple[FFProbeStream, ...]
    """
    The media streams info.
    """
