import os
from dataclasses import asdict
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from ..info import detect, generate_thumbnail


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in (Path(__file__).parent.parent / "utils/tests").glob("data/*")],
)
def test_detect(case: Path, snapshot: SnapshotAssertion) -> None:
    # NOTE:
    # because we use docker to run ffmpeg, the input path need to be relative to the current working directory
    info = detect(str(case.relative_to(Path.cwd())))
    snapshot(extension_class=JSONSnapshotExtension) == asdict(info)

    if info.type in ("video", "image"):
        assert os.path.exists(generate_thumbnail(str(case.relative_to(Path.cwd())), "tmp.png"))
