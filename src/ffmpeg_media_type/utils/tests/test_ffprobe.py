from dataclasses import asdict
from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.filters import paths

from ...conftest import sample_test_media_files
from ..ffprobe import ffprobe


@pytest.mark.parametrize("case", sample_test_media_files())
def test_ffprobe_file(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot(extension_class=JSONSnapshotExtension, exclude=paths("format.filename")) == asdict(ffprobe(str(case.relative_to(Path.cwd()))))
