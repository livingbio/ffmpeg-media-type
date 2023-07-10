from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from syrupy.assertion import SnapshotAssertion

from ..table import table_to_2d


@pytest.mark.parametrize("case", Path(__file__).parent.glob("test_table/*.html"))
def test_table_to_2d(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot == table_to_2d(BeautifulSoup(case.read_text(), "html.parser"))
