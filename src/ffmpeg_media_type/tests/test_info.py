import os
from dataclasses import asdict
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

from ..conftest import sample_test_media_files
from ..info import detect, generate_thumbnail


@pytest.mark.parametrize("case", sample_test_media_files())
def test_detect(case: Path, snapshot: SnapshotAssertion) -> None:
    # NOTE:
    # because we use docker to run ffmpeg, the input path need to be relative to the current working directory
    info = detect(str(case.relative_to(Path.cwd())))
    snapshot(extension_class=JSONSnapshotExtension) == asdict(info)

    if info.type in ("video", "image"):
        assert os.path.exists(generate_thumbnail(str(case.relative_to(Path.cwd())), "tmp.png"))
