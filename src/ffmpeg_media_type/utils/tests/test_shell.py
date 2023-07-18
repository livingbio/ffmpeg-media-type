from syrupy.assertion import SnapshotAssertion

from ..shell import call


def test_call(snapshot: SnapshotAssertion) -> None:
    assert snapshot == call(["echo", "hello world"])
