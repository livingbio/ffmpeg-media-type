from itertools import product

from bs4 import BeautifulSoup

# credit https://stackoverflow.com/questions/48393253/how-to-parse-table-with-rowspan-and-colspan/48451104#48451104


def table_to_2d(table_str: str) -> list[list[str | None]]:
    table_tag = BeautifulSoup(table_str, "html.parser")
    rowspans: list[int] = []  # track pending rowspans
    rows = table_tag.find_all("tr")

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(["td", "th"], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1.
        # a colspan of 0 means “fill until the end” but can really only apply
        # to the last cell; ignore it elsewhere.
        colcount = max(
            colcount,
            sum(int(c.get("colspan", 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans),
        )
        # update rowspan bookkeeping; 0 is a span to the bottom.
        rowspans += [int(c.get("rowspan", 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table: list[list[str | None]] = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans_dict: dict[int, int] = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans
        for col, cell in enumerate(row_elem.find_all(["td", "th"], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans_dict.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans_dict[col] = int(cell.get("rowspan", 1)) or len(rows) - row
            colspan = int(cell.get("colspan", 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans_dict[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans_dict = {c: s - 1 for c, s in rowspans_dict.items() if s > 1}

    return table
