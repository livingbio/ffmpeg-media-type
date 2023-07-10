from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ..table import table_to_2d
from ..wiki_ext import _extract_wiki_ext_info, extract_tables_from_wikipedia


@pytest.mark.parametrize(
    "case",
    [pytest.param(k, id=k.name) for k in Path(__file__).parent.glob("test_wiki_ext/*.html")],
)
def test_extract_tables_from_wikipedia(snapshot: SnapshotAssertion, case: Path) -> None:
    tables = extract_tables_from_wikipedia(case.read_text())

    assert snapshot(name=case.name) == tables

    for table in tables:
        assert snapshot == table_to_2d(table)


@pytest.mark.vcr
def test__extract_wiki_ext_info(snapshot: SnapshotAssertion) -> None:
    url = "https://en.wikipedia.org/wiki/List_of_filename_extensions_(S%E2%80%93Z)"
    ext_infos = _extract_wiki_ext_info(url)

    assert snapshot == ext_infos

    # check rowspan is handled correctly
    tze = [k for k in ext_infos if k.ext.lower() == "tz2"]
    assert len(tze) == 1, tze
    assert tze[0].used_by == "tar and other file archivers with support"
