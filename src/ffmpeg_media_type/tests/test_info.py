import os
import tempfile
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from ..info import detect, generate_thumbnail


@pytest.mark.ffmpeg_version
@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in (Path(__file__).parent.parent / "utils/tests").glob("test_ffmpeg/*")],
)
def test_detect(case: Path, snapshot_ffmpeg: SnapshotAssertion) -> None:
    info = detect(str(case.relative_to(Path.cwd())))
    snapshot_ffmpeg(name=case.name, exclude=props("duration")) == info.dict()

    if info.type in ("video", "image"):
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        thumbnail_path = os.path.join(temp_dir, f"{case.name}.thumbnail.jpg")  # Temporary thumbnail file path
        generate_thumbnail(str(case), thumbnail_path)
