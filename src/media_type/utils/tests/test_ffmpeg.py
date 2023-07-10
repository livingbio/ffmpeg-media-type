from syrupy.assertion import SnapshotAssertion

from ..ffmpeg import list_support_format


def test_list_support_format(snapshot: SnapshotAssertion) -> None:
    assert snapshot == list_support_format()
