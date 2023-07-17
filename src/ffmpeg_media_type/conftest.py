from pathlib import Path


def sample_cases() -> list[Path]:
    return [k for k in (Path(__file__).parent / "tests/data/").glob("**/*") if k.is_file()]
