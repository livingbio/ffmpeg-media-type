from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ...conftest import sample_test_media_files
from ...exceptions import FfmpegMediaTypeError
from ..hotfix_webp import extract_animated_webp_frame, is_webp_animated


@pytest.mark.parametrize("case", sample_test_media_files("54/*"))
def test_is_webp_animated(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot == is_webp_animated(case)


@pytest.mark.parametrize("case", sample_test_media_files("54/*"))
def test_extract_animated_webp_frame(case: Path, snapshot: SnapshotAssertion) -> None:
    try:
        extract_animated_webp_frame(case)
        assert snapshot == True
    except FfmpegMediaTypeError:
        assert snapshot == False
