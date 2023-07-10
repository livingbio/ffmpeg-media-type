from syrupy.assertion import SnapshotAssertion

from ..ffmpeg import _get_muxer_info, list_support_format


def test_list_support_format(snapshot: SnapshotAssertion) -> None:
    assert snapshot == list_support_format()


def test__get_muxer_info(snapshot: SnapshotAssertion) -> None:
    assert snapshot == _get_muxer_info("E", "mp4", "MP4 (MPEG-4 Part 14)")
