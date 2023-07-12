import os
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ..ffmpeg import _cache_file, _generate_cache, _get_muxer_info, _load_cache, ffprobe_file, get_ffmpeg_version, list_support_format


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
def test_ffprobe_file(case: Path) -> None:
    ffprobe_file(str(case))


def test_generate_cache() -> None:
    cache_file = _cache_file("6.0")
    if os.path.exists(cache_file):
        os.remove(cache_file)

    _generate_cache("6.0")
    infos = _load_cache("6.0")
    assert len(infos) > 0
    assert os.path.exists(cache_file)
