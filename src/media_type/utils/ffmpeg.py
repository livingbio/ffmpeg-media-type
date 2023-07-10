import os
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class FFMpegSupport:
    demuxing_support: bool
    muxing_support: bool
    codec: str
    description: str

    common_exts: list[str]
    mime_type: str
    default_video_codec: str
    default_audio_codec: str


def _parse_muxer_info(content: str) -> dict[str, Any]:
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


def _get_muxer_info(flag: str, codec: str, description: str) -> FFMpegSupport:
    muxer_info = {
        "common_exts": [],
        "mime_type": "",
        "default_video_codec": "",
        "default_audio_codec": "",
    }
    if "E" in flag:
        os.system(f"ffmpeg -h muxer={codec} > output")
        muxer_info.update(_parse_muxer_info(open("output").read()))
    if "D" in flag:
        os.system(f"ffmpeg -h demuxer={codec} > output")
        muxer_info.update(_parse_muxer_info(open("output").read()))

    return FFMpegSupport(
        demuxing_support="D" in flag,
        muxing_support="E" in flag,
        codec=codec,
        description=description,
        **muxer_info,  # type: ignore[arg-type]
    )


def list_support_format() -> tuple[str, list[FFMpegSupport]]:
    os.system("ffmpeg -formats &> format.txt")

    re_ffmpeg_version = re.compile(r"ffmpeg version (?P<version>[\d\.]+)")

    re_ffmpeg_support_file_format = re.compile(r"(?P<flag>[DE]+)[\s]+(?P<codec>[\w\d,]+)[\s]+(?P<description>.*)")

    with open("format.txt") as ifile:
        content = ifile.read()

    match_version = re_ffmpeg_version.findall(content)
    assert match_version and len(match_version) == 1, match_version
    version = match_version[0]

    print(f"FFMpeg version: {version}")

    support_infos = re_ffmpeg_support_file_format.findall(content)
    output = []
    for support_info in support_infos:
        flag, codec, description = support_info
        output.append(_get_muxer_info(flag, codec, description))

    return version, output
