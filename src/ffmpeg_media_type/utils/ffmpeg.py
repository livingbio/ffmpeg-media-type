import json
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


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
        os.system(f"docker run jrottenberg/ffmpeg:{version}-scratch -h muxer={codec} > output 2>&1")
        muxer_info.update(_parse_muxer_info(open("output").read()))
    if "D" in flag:
        os.system(f"docker run jrottenberg/ffmpeg:{version}-scratch -h demuxer={codec} > output 2>&1")
        muxer_info.update(_parse_muxer_info(open("output").read()))

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
    os.system(f"docker run jrottenberg/ffmpeg:{version}-scratch -formats > format.txt 2>&1")

    with open("format.txt") as ifile:
        content = ifile.read()

    # print(f"FFMpeg version: {version}")

    support_infos = _extract_file_format(content)
    output = []
    for support_info in support_infos:
        flag, codec, description = support_info
        output.append(_get_muxer_info(version, flag, codec, description))

    return output


def _cache_file(version: str) -> str:
    major_minor_version = ".".join(version.split(".")[:2])
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


@lru_cache
def get_ffmpeg_version() -> str:
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, shell=True)
        output_lines = result.stdout.strip().split("\n")
        version_line = output_lines[0].strip()
        version = version_line.split(" ")[2]
        return version
    except FileNotFoundError as e:
        raise FileNotFoundError("FFmpeg not found") from e


def ffprobe(input_url: str) -> FFProbeInfo:
    # Construct the FFprobe command with JSON output format
    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        input_url,
    ]

    try:
        # Execute the FFprobe command and capture the output
        output = subprocess.check_output(ffprobe_cmd, stderr=subprocess.STDOUT, shell=True)
        output_str = output.decode("utf-8")  # Convert bytes to string
        return FFProbeInfo(**json.loads(output_str))
    except subprocess.CalledProcessError as e:
        # print(f"FFprobe error: {e.output}")
        raise
