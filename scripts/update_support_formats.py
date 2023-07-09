import csv
import os
import re
from collections import defaultdict

import yaml
import typer


def extract_wiki():
    # DATA Source:
    # 'https://en.wikipedia.org/wiki/List_of_filename_extensions'
    # 'https://en.wikipedia.org/wiki/List_of_filename_extensions_(A%E2%80%93E)'
    # 'https://en.wikipedia.org/wiki/List_of_filename_extensions_(F%E2%80%93L)'
    # 'https://en.wikipedia.org/wiki/List_of_filename_extensions_(M%E2%80%93R)'
    # 'https://en.wikipedia.org/wiki/List_of_filename_extensions_(S%E2%80%93Z)'
    # and extract by http://wikitable2csv.ggor.de/

    result = defaultdict(list)
    with open("wiki_table.csv") as ifile:
        irows = csv.DictReader(ifile)
        for irow in irows:
            if irow["Ext."] == "Ext.":
                continue

            result[irow["Ext."].lower()].append(
                "%s Used by %s" % (irow["Description"], irow["Used by"])
            )

    return result


def list_support_format():
    os.system("ffmpeg -formats > format.txt")

    pattern = re.compile(
        r"(?P<flag>[DE]+)[\s]+(?P<codec>[\w\d,]+)[\s]+(?P<description>.*)"
    )
    ext_pattern = re.compile(r"Common extensions: ([\w\d\,]+)\.")

    output = {}

    wiki_result = extract_wiki()

    with open("format.txt") as ifile:
        for iline in ifile:
            match = pattern.search(iline)
            if not match:
                continue

            format = match.groupdict()
            codec = format["codec"]

            os.system("ffmpeg -h muxer=%s > output" % codec)

            with open("output") as ext:
                r = ext_pattern.findall(ext.read())

                if r:
                    output[codec] = {
                        "exts": r[0].split(","),
                        "description": format["description"],
                        "enable": True,
                    }
                elif codec.endswith("_pipe"):
                    output[codec] = {
                        "exts": [codec.replace("_pipe", "")],
                        "description": codec,
                        "enable": True,
                    }
                elif codec in wiki_result:
                    output[codec] = {
                        "exts": [codec],
                        "description": ",".join(wiki_result[codec]) + " (wiki)",
                        "enable": True,
                    }
                else:
                    output[codec] = {"enable": False}

    with open("support_formats.yml", "w") as ofile:
        yaml.dump(output, ofile)


if __name__ == "__main__":
    typer.run(list_support_format)
