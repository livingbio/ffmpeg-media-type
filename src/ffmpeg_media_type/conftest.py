from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pytest

TEST_DATA_FOLDER = Path(__file__).parent / "test_data"


def sample_test_media_files(pattern: str = "**/*") -> Iterable[Any]:
    for f in TEST_DATA_FOLDER.glob(pattern):
        if f.is_file():
            yield pytest.param(f, id=f.name)
