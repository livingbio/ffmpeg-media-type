from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from ..info import detect


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in (Path(__file__).parent.parent / "utils/tests").glob("test_ffmpeg/*")],
)
def test_detect(case: Path, snapshot: SnapshotAssertion) -> None:
    snapshot(name=case.name, exclude=props("duration")) == detect(str(case)).dict()
