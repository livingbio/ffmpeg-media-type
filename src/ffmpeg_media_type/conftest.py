from pathlib import Path
from typing import Any, Iterable

import pytest


def sample_test_media_files() -> Iterable[Any]:
    for f in (Path(__file__).parent / "test_data").glob("**/*"):
        if f.is_file():
            yield pytest.param(f, id=f.name)
