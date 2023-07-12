import typer

from .utils.ffmpeg import _generate_cache


def main() -> None:
    versions = [
        "3.2",
        "3.3",
        "3.4",
        "4.0",
        "4.1",
        "4.2",
        "4.3",
        "4.4",
        "5.0",
        "5.1",
        "6.0",
    ]

    for version in versions:
        _generate_cache(version)


if __name__ == "__main__":
    typer.run(main)
