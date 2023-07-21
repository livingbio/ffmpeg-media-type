from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation

from .utils.ffmpeg import get_ffmpeg_version


@pytest.fixture(scope="session")
def ffmpeg_version() -> str:
    return get_ffmpeg_version("minor")


class DifferentDirectoryExtension(AmberSnapshotExtension):
    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        version = get_ffmpeg_version("minor")
        return str(Path(test_location.filepath).parent / "__snapshots__" / version)


@pytest.fixture
def snapshot_ffmpeg(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.use_extension(DifferentDirectoryExtension)
