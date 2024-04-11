import os
from pathlib import Path
from unittest import mock

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import paths

from .. import ffmpeg
from ..ffmpeg import _cache_file, _generate_cache, _get_muxer_info, _load_cache, ffprobe, get_ffmpeg_version, list_support_format


def test_list_support_format(snapshot: SnapshotAssertion) -> None:
    assert snapshot == list_support_format("6.0")


def test__get_muxer_info(snapshot: SnapshotAssertion) -> None:
    assert snapshot == _get_muxer_info("6.0", "E", "mp4", "MP4 (MPEG-4 Part 14)")


def test_load_cache() -> None:
    cache_file_6_1 = _cache_file("6.1")
    cache_file_6_1_1 = _cache_file("6.1.1")

    assert cache_file_6_1 == cache_file_6_1_1


def test_generate_cache() -> None:
    cache_file = _cache_file("6.1")
    if os.path.exists(cache_file):
        os.remove(cache_file)

    _generate_cache("6.1")
    infos = _load_cache("6.1")
    assert len(infos) > 0
    assert os.path.exists(cache_file)


@pytest.mark.parametrize("mode", ["major", "minor", "patch"])
def test_get_ffmpeg_version(mode: str, snapshot: SnapshotAssertion) -> None:
    with mock.patch(ffmpeg.__name__ + ".call", return_value="ffmpeg version 4.2.2") as call:
        # NOTE: mock the call function to avoid calling the real ffmpeg
        # NOTE: use __wrapped__ to get the original function since it is wrapped by lru_cache
        assert snapshot == get_ffmpeg_version.__wrapped__(mode)
        assert call.called


@pytest.mark.ffmpeg_version
@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in Path(__file__).parent.glob("test_ffmpeg/*")],
)
def test_ffprobe_file(case: Path, snapshot_ffmpeg: SnapshotAssertion) -> None:
    assert snapshot_ffmpeg(name=case.name, exclude=paths("format.filename")) == ffprobe(str(case.relative_to(Path.cwd()))).dict()
