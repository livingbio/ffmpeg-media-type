from pathlib import Path


def ffmpeg_sample_files() -> list[Path]:
    return [k for k in (Path(__file__).parent / "tests/data/").glob("**/*") if k.is_file()]
