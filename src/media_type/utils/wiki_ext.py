import re
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from .table import table_to_2d


class ExtInfo(BaseModel):
    ext: str
    description: str
    used_by: str


def extract_tables_from_wikipedia(html: str) -> List[str]:
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    # Find all table elements on the page
    tables = soup.find_all("table", class_="wikitable")

    return [str(k) for k in tables]


urls = [
    "https://en.wikipedia.org/wiki/List_of_filename_extensions_(0%E2%80%939)",
    "https://en.wikipedia.org/wiki/List_of_filename_extensions_(A%E2%80%93E)",
    "https://en.wikipedia.org/wiki/List_of_filename_extensions_(F%E2%80%93L)",
    "https://en.wikipedia.org/wiki/List_of_filename_extensions_(M%E2%80%93R)",
    "https://en.wikipedia.org/wiki/List_of_filename_extensions_(S%E2%80%93Z)",
]


def __remove_note(text: str | None) -> str:
    if text:
        return re.sub(r"\[\d*\]", "", text.strip())
    return ""


def _extract_wiki_ext_info(url: str) -> list[ExtInfo]:
    # Extract tables from the Wikipedia page

    html = requests.get(url).text
    tables = extract_tables_from_wikipedia(html)
    output = []
    for table in tables:
        normalize_table = table_to_2d(table)

        for row in normalize_table[1:]:
            output.append(
                ExtInfo(
                    ext=__remove_note(row[0]),
                    description=__remove_note(row[1]),
                    used_by=__remove_note(row[2]),
                )
            )

    return output


def extract_wiki_filename_exts() -> list[ExtInfo]:
    output = []
    for url in urls:
        output.extend(_extract_wiki_ext_info(url))

    return output
