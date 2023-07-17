import os
import tempfile
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from ..conftest import sample_cases
from ..info import detect, generate_thumbnail


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in sample_cases()],
)
def test_detect(case: Path, snapshot: SnapshotAssertion) -> None:
    # NOTE: store the parent folder name as the media type
    _type = case.parent.name

    info = detect(str(case))

    assert info.type == _type, f"expect type {_type}, got {info.type} for {case}"

    # NOTE: exclude duration from snapshot because it is not stable in different ffmpeg versions
    snapshot(name=case.name, exclude=props("duration")) == info.dict()

    if info.type in ("video", "image"):
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        thumbnail_path = os.path.join(temp_dir, f"{case.name}.thumbnail.jpg")  # Temporary thumbnail file path
        generate_thumbnail(str(case), thumbnail_path)
