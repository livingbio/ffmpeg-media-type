from dataclasses import asdict
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import paths

from ..ffmpeg import _get_muxer_info, ffprobe_file, get_ffmpeg_version, list_support_format


def test_list_support_format(snapshot: SnapshotAssertion) -> None:
    assert snapshot == list_support_format("6.0")


def test__get_muxer_info(snapshot: SnapshotAssertion) -> None:
    assert snapshot == _get_muxer_info("6.0", "E", "mp4", "MP4 (MPEG-4 Part 14)")


def test_get_ffmpeg_version() -> None:
    get_ffmpeg_version()


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in Path(__file__).parent.glob("test_ffmpeg/*")],
)
def test_ffprobe_file(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot(name=case.name, exclude=paths("format.filename")) == asdict(ffprobe_file(str(case)))
