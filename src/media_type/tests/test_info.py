from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ..info import detect


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in (Path(__file__).parent.parent / "utils/tests").glob("test_ffmpeg/*")],
)
def test_detect(case: Path, snapshot: SnapshotAssertion) -> None:
    snapshot.assert_match(detect(str(case)))
