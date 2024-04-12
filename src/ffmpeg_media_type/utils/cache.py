import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import TypeVar

cache_path = Path(__file__).parent / "cache"
cache_path.mkdir(exist_ok=True)

T = TypeVar("T")


def load(cls: type[T], name: str) -> T | None:
    path = cache_path / f"{name}.json"

    if not path.exists():
        return None

    with path.open() as ifile:
        return cls(**json.loads(ifile.read()))


def save(obj: T, name: str) -> None:
    assert is_dataclass(obj) and not isinstance(obj, type)

    with (cache_path / f"{name}.json").open("w") as ofile:
        ofile.write(json.dumps(asdict(obj)))
