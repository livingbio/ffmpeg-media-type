import os
import re
from dataclasses import dataclass


@dataclass
class FFMpegSupport:
    demuxing_support: bool
    muxing_support: bool
    codec: str
    description: str


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
        output.append(
            FFMpegSupport(
                demuxing_support="D" in flag,
                muxing_support="E" in flag,
                codec=codec,
                description=description,
            )
        )
    return version, output
