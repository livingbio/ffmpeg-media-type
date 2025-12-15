from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion

from ...conftest import sample_test_media_files
from ...exceptions import FFmpegMediaTypeError
from ..hotfix_webp import (
    check_webpmux_installed,
    extract_animated_webp_frame,
    hotfix_animate_webp,
    is_webp_animated,
)

# Skip tests if webpmux is not installed
webpmux_installed = check_webpmux_installed() is not None
requires_webpmux = pytest.mark.skipif(not webpmux_installed, reason="webpmux not installed")


@requires_webpmux
@pytest.mark.parametrize("case", sample_test_media_files("54/*"))
def test_is_webp_animated(case: Path, snapshot: SnapshotAssertion) -> None:
    assert snapshot == is_webp_animated(str(case))


@requires_webpmux
@pytest.mark.parametrize("case", sample_test_media_files("54/*"))
def test_extract_animated_webp_frame(case: Path, snapshot: SnapshotAssertion) -> None:
    try:
        extract_animated_webp_frame(str(case))
        assert snapshot == True  # noqa: E712
    except FFmpegMediaTypeError:
        assert snapshot == False  # noqa: E712


@requires_webpmux
@pytest.mark.parametrize("case", sample_test_media_files("54/*"))
def test_hotfix_animate_webp(case: Path, snapshot: SnapshotAssertion) -> None:
    result = hotfix_animate_webp(case)

    assert not is_webp_animated(result)
