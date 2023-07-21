import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from .shell import call


class FFProbeFormat(BaseModel):
    filename: str | None = None
    duration: float | None = None
    format_name: str | None = None
    format_long_name: str | None = None
    start_time: float | None = None
    size: int | None = None
    probe_score: int | None = None

    class Config:
        extra = "allow"


class FFProbeStreamTags(BaseModel):
    rotate: int = 0

    class Config:
        extra = "allow"


class FFProbeStream(BaseModel):
    index: int | None = None
    width: int | None = None
    height: int | None = None
    codec_type: str | None = None
    codec_name: str | None = None
    codec_long_name: str | None = None
    profile: str | None = None
    pix_fmt: str | None = None
    r_frame_rate: str | None = None
    tags: FFProbeStreamTags = Field(default_factory=FFProbeStreamTags)

    class Config:
        extra = "allow"


class FFProbeInfo(BaseModel):
    format: FFProbeFormat
    streams: list[FFProbeStream]

    class Config:
        extra = "allow"


class FFMpegSupport(BaseModel):
    demuxing_support: bool
    muxing_support: bool
    codec: str
    description: str

    common_exts: list[str]
    mime_type: str
    default_video_codec: str
    default_audio_codec: str


def _parse_muxer_info(content: str) -> dict[str, Any]:
    # print(f"{content=}")
    re_ext_pattern = re.compile(r"Common extensions: ([\w\d\,]+)\.")
    re_mime_type_pattern = re.compile(r"Mime type: ([\w\d\/\-\+]+)")
    re_default_video_codec_pattern = re.compile(r"Default video codec: ([\w\d\/\-\+]+)")
    re_default_audio_codec_pattern = re.compile(r"Default audio codec: ([\w\d\/\-\+]+)")

    output = {}
    if exts := re_ext_pattern.findall(content):
        output["common_exts"] = exts[0].split(",")
    if mime_type := re_mime_type_pattern.findall(content):
        output["mime_type"] = mime_type[0]
    if default_video_codec := re_default_video_codec_pattern.findall(content):
        output["default_video_codec"] = default_video_codec[0]
    if default_audio_codec := re_default_audio_codec_pattern.findall(content):
        output["default_audio_codec"] = default_audio_codec[0]

    return output


def _get_muxer_info(version: str, flag: str, codec: str, description: str) -> FFMpegSupport:
    muxer_info = {
        "common_exts": [],
        "mime_type": "",
        "default_video_codec": "",
        "default_audio_codec": "",
    }
    if "E" in flag:
        text = call(
            [
                "docker",
                "run",
                f"jrottenberg/ffmpeg:{version}-scratch",
                "-h",
                f"muxer={codec}",
            ]
        )
        muxer_info.update(_parse_muxer_info(text))
    if "D" in flag:
        text = call(
            [
                "docker",
                "run",
                f"jrottenberg/ffmpeg:{version}-scratch",
                "-h",
                f"demuxer={codec}",
            ]
        )
        muxer_info.update(_parse_muxer_info(text))

    # print(f"{codec=}, {muxer_info=}")
    return FFMpegSupport(
        demuxing_support="D" in flag,
        muxing_support="E" in flag,
        codec=codec,
        description=description,
        **muxer_info,  # type: ignore[arg-type]
    )


def _extract_file_format(content: str) -> list[tuple[str, str, str]]:
    re_ffmpeg_support_file_format = re.compile(r"(?P<flag>[DE]+)[\s]+(?P<codec>[\w\d,]+)[\s]+(?P<description>[^\n]*)")
    output = []
    for iline in content.split("\n"):
        support_infos = re_ffmpeg_support_file_format.findall(iline)

        if support_infos:
            output.append(support_infos[0])
    return output


def list_support_format(version: str) -> list[FFMpegSupport]:
    content = call(["docker", "run", f"jrottenberg/ffmpeg:{version}-scratch", "-formats"])

    # print(f"FFMpeg version: {version}")

    support_infos = _extract_file_format(content)
    output = []
    for support_info in support_infos:
        flag, codec, description = support_info
        output.append(_get_muxer_info(version, flag, codec, description))

    return output


def _cache_file(version: str) -> str:
    major_minor_version = get_ffmpeg_version("minor")
    return str(Path(__file__).parent.parent / "data" / f"ffmpeg-{major_minor_version}.json")


def _generate_cache(version: str) -> None:
    infos = list_support_format(version)

    with open(_cache_file(version), "w") as ofile:
        ofile.write(json.dumps([k.dict() for k in infos], indent=4))


@lru_cache
def _load_cache(version: str) -> list[FFMpegSupport]:
    with open(_cache_file(version)) as ifile:
        return [FFMpegSupport(**k) for k in json.load(ifile)]


def load_cache() -> dict[str, FFMpegSupport]:
    ffmpeg_version = get_ffmpeg_version()
    output = {}
    for info in _load_cache(ffmpeg_version):
        output[info.codec] = info

    return output


def get_ffprobe() -> list[str]:
    version = os.environ.get("FFMPEG_DOCKER_VERSION")
    if version:
        return [
            "docker",
            "run",
            "--entrypoint",
            "ffprobe",
            "-v",
            f"{Path.cwd()}:/work",
            "-w",
            "/work",
            f"jrottenberg/ffmpeg:{version}-scratch",
        ]
    return ["ffprobe"]


def get_ffmpeg() -> list[str]:
    version = os.environ.get("FFMPEG_DOCKER_VERSION")
    if version:
        return [
            "docker",
            "run",
            "--entrypoint",
            "ffmpeg",
            "-v",
            f"{Path.cwd()}:/work",
            "-w",
            "/work",
            f"jrottenberg/ffmpeg:{version}-scratch",
        ]
    return ["ffmpeg"]


@lru_cache
def get_ffmpeg_version(mode: Literal["major", "minor", "patch"] = "patch") -> str:
    result = call(get_ffmpeg() + ["-version"])

    try:
        m_version = re.findall(r"ffmpeg version ([\d\.]+)", result)
        assert len(m_version) == 1, m_version
        version = m_version[0]

        v_parts = version.split(".")
        assert len(v_parts) <= 3, f"version format error: {version}"

        v_parts += ["0"] * (3 - len(v_parts))

        if mode == "patch":
            v_parts = v_parts[:3]
        elif mode == "minor":
            v_parts = v_parts[:2]
        else:
            v_parts = v_parts[:1]

        return ".".join(v_parts)

    except IndexError as e:
        raise RuntimeError(f"FFmpeg version not found {result}") from e


def ffprobe(input_url: str) -> FFProbeInfo:
    # Construct the FFprobe command with JSON output format
    ffprobe_cmd = get_ffprobe() + [
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
    return FFProbeInfo(**json.loads(output))
