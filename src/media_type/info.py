from dataclasses import dataclass
from typing import Literal


@dataclass
class MediaInfo:
    type: Literal["image", "video", "audio"]

    width: int | None = None
    height: int | None = None
    duration: float | None = None

    format: str | None = None
    size: int | None = None
    suggest_ext: str | None = None


def detect(uri: str) -> None:
    ...
