import requests
from bs4 import BeautifulSoup
from typing import List

def extract_tables_from_wikipedia(url: str) -> List[List[List[str]]]:
    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all table elements on the page
    tables = soup.find_all("table", class_="wikitable")

    extracted_tables = []
    # Extract the data from each table
    for table in tables:
        table_data = []
        for row in table.find_all("tr"):
            row_data = []
            for cell in row.find_all(["th", "td"]):
                row_data.append(cell.text.strip())
            table_data.append(row_data)

        extracted_tables.append(table_data)

    return extracted_tables

# URL of the Wikipedia page
urls = [
    'https://en.wikipedia.org/wiki/List_of_filename_extensions',
    'https://en.wikipedia.org/wiki/List_of_filename_extensions_(A%E2%80%93E)',
    'https://en.wikipedia.org/wiki/List_of_filename_extensions_(F%E2%80%93L)',
    'https://en.wikipedia.org/wiki/List_of_filename_extensions_(M%E2%80%93R)',
    'https://en.wikipedia.org/wiki/List_of_filename_extensions_(S%E2%80%93Z)'
]

for url in urls:
    # Extract tables from the Wikipedia page
    tables = extract_tables_from_wikipedia(url)

    # Print the table data
    for table_data in tables:
        for row in table_data:
            print(row)
        print("\n")  # Add a line break between tables
    # 