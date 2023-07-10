import dataclasses
import json

import typer

from .utils.ffmpeg import list_support_format


def generate(version: str) -> None:
    infos = list_support_format(version)

    with open(f"data/ffmpeg-{version}.json", "w") as ofile:
        ofile.write(json.dumps([dataclasses.asdict(k) for k in infos], indent=4))


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
        generate(version)


if __name__ == "__main__":
    typer.run(main)
