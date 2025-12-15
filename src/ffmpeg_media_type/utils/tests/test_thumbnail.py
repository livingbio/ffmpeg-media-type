from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ...conftest import sample_test_media_files
from ...exceptions import FFmpegMediaTypeError
from ..thumbnail import generate_thumbnail


@pytest.mark.parametrize("case", sample_test_media_files())
def test_thumbnail(case: Path, snapshot: SnapshotAssertion) -> None:
    try:
        generate_thumbnail(case)
        assert snapshot
    except FFmpegMediaTypeError:
        assert not snapshot
