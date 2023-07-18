import os
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ...conftest import ffmpeg_sample_files
from ..ffmpeg import _cache_file, _generate_cache, _get_muxer_info, _load_cache, ffprobe, get_ffmpeg_version, list_support_format


@pytest.mark.integration
def test_list_support_format(snapshot: SnapshotAssertion) -> None:
    assert snapshot == list_support_format("6.0")


@pytest.mark.integration
def test__get_muxer_info(snapshot: SnapshotAssertion) -> None:
    assert snapshot == _get_muxer_info("6.0", "E", "mp4", "MP4 (MPEG-4 Part 14)")


def test_get_ffmpeg_version(snapshot: SnapshotAssertion) -> None:
    version = get_ffmpeg_version()
    assert snapshot(name=version) == get_ffmpeg_version()


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in ffmpeg_sample_files()],
)
def test_ffprobe_file(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot == ffprobe(str(case))


def test_generate_cache() -> None:
    cache_file = _cache_file("6.0")
    if os.path.exists(cache_file):
        os.remove(cache_file)

    _generate_cache("6.0")
    infos = _load_cache("6.0")
    assert len(infos) > 0
    assert os.path.exists(cache_file)
