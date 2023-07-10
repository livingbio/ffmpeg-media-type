import dataclasses
import json

import typer

from .utils.ffmpeg import list_support_format


def main() -> None:
    version, infos = list_support_format()

    with open(f"data/ffmpeg-{version}.json", "w") as ofile:
        ofile.write(json.dumps([dataclasses.asdict(k) for k in infos], indent=4))


if __name__ == "__main__":
    typer.run(main)
