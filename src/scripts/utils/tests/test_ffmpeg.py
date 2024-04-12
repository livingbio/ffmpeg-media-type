from ..ffmpeg import _get_muxer_info, list_support_format


def test_list_support_format() -> None:
    assert len(list_support_format()) > 0


def test__get_muxer_info() -> None:
    assert _get_muxer_info(["ffmpeg"], "E", "mp4", "MP4 (MPEG-4 Part 14)")
