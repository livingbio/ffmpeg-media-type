import re
from typing import Any

from ffmpeg_media_type.schema import FFMpegSupport


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


def _get_muxer_info(cmds: list[str], flag: str, codec: str, description: str) -> FFMpegSupport:
    muxer_info = {
        "common_exts": [],
        "mime_type": "",
        "default_video_codec": "",
        "default_audio_codec": "",
    }

    if "E" in flag:
        text = _call(
            cmds
            + [
                "-hide_banner",
                "-h",
                f"muxer={codec}",
            ]
        )
        muxer_info.update(_parse_muxer_info(text))

    if "D" in flag:
        text = _call(
            cmds
            + [
                "-hide_banner",
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


def list_support_format(cmds: list[str] = ["ffmpeg"]) -> list[FFMpegSupport]:
    """
    List all supported formats by ffmpeg.

    Args:
        cmds: Defaults to ["ffmpeg"].

    Returns:
        List of supported formats.
    """
    content = _call(cmds + ["-formats"])

    support_infos = _extract_file_format(content)
    output = []
    for support_info in support_infos:
        flags, codec, description = support_info
        output.append(_get_muxer_info(cmds, flags, codec, description))

    return output
