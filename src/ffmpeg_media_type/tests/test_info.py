from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ..info import detect, generate_thumbnail


@pytest.mark.ffmpeg_version
@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in (Path(__file__).parent.parent / "utils/tests").glob("test_ffmpeg/*")],
)
def test_detect(case: Path, snapshot_ffmpeg: SnapshotAssertion) -> None:
    # NOTE:
    # because we use docker to run ffmpeg, the input path need to be relative to the current working directory

    info = detect(str(case.relative_to(Path.cwd())))
    snapshot_ffmpeg(name=case.name) == info.dict()

    if info.type in ("video", "image"):
        generate_thumbnail(str(case.relative_to(Path.cwd())), "tmp.png")
