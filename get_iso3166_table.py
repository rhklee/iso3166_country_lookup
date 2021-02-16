import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Tuple
import json


RAW_HTML_SOURCE = 'https://gist.githubusercontent.com/rhklee/8ccb4a853428e44be2fc9ced7b5d5325/raw/2f0634456b98d01db9190bbe62f500f04e20a2bd/iso3166.html'


def get_raw_data(source: str = RAW_HTML_SOURCE) -> str:
    r = requests.get(source)
    if r.status_code != 200:
        raise Exception("There was an error fetching the source from {}".format(source))
    return r.text


def get_soup(data: str):
    return BeautifulSoup(data, features = "html.parser")


def get_cols(row, col_el: str) -> List[str]:
    return [ col.get_text() for col in row.find_all(col_el) ]


def parse_data(soup) -> Tuple[List[str], List[List[str]]]:
    rows = soup.find_all('tr')

    header_row = rows[0]
    data_rows = rows[1:]

    headers = get_cols(header_row, 'th')
    data = [ get_cols(data_row, 'td') for data_row in data_rows ]

    return (headers, data)


def write_csv(rows: List[List[str]], filename: str = 'iso3166.csv') -> None:
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)


def write_json(data: List[List[str]]) -> None:
    alpha2 = {}
    alpha3 = {}
    numeric3 = {}

    for row in data:
        all_row_data = row[0:1] + row[2:]
        alpha2[row[2]] = all_row_data
        alpha3[row[3]] = all_row_data
        numeric3[row[4]] = all_row_data

    with open('alpha2.json', 'w') as a2, \
            open('alpha3.json', 'w') as a3, \
            open('numeric3.json', 'w') as n3:
        a2.write(json.dumps(alpha2))
        a3.write(json.dumps(alpha3))
        n3.write(json.dumps(numeric3))


def main() -> None:
    soup = get_soup(get_raw_data())
    # (headers, data) = parse_data(soup)
    # write_csv([ headers ] + data)

    (_, data) = parse_data(soup)
    write_json(data)


if __name__ == "__main__":
    main()