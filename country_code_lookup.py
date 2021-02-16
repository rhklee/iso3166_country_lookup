import json
import argparse
from typing import List


def parse_args() -> str:
    ap = argparse.ArgumentParser(prog='country_code_lookup', description='Conveniently look up ISO 3166 country codes.')

    ap.add_argument('code', metavar='country_code', type=str, help='A ISO 3166 country code (alpha 2, alpha 3, or numeric).')

    return ap.parse_args()


def row_printer(row: List[str]) -> None:
    print('\n'.join(row))


def pad(num: str) -> str:
    return '0' * (3 - len(num)) + num


def lookup(code: str):
    cs = code.strip().upper()
    with open('alpha2.json', 'r') as a2:
        alpha2 = json.loads(a2.read())
        if cs in alpha2:
            row_printer(alpha2[cs])
            return
    with open('alpha3.json', 'r') as a3:
        alpha3 = json.loads(a3.read())
        if cs in alpha3:
            row_printer(alpha3[cs])
            return
    with open('numeric3.json', 'r') as n3:
        numeric3 = json.loads(n3.read())
        cs_num = pad(cs)
        if cs_num in numeric3:
            row_printer(numeric3[cs_num])
            return

    print(f'No ISO 3166 was found for {code}')


def main() -> None:
    args = parse_args()
    lookup(args.code)


if __name__ == '__main__':
    main()