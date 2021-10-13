import json
import re

PATTERN_DCT = {
    "telephone": r'[+]\d-[(]\d{3}[)]-\d{3}-\d{2}-\d{2}',
    "weight": r'\d{2,3}',
    "inn": r'\d{12}',
    "passport_series": r'\d{2} \d{2}',
    "occupation": r'[А-Яа-яЁё ]+?',
    "age": r'\d{2}',
    "political_views": r'[А-Яа-яЁё ]+?',
    "worldview": r'[А-Яа-яЁё ]+?',
    "address": r'[А-Яа-яЁё .]+? \d+?'
}
invalid_count = 0


class Reader:
    @staticmethod
    def read_json(path: str) -> dict:
        f = open(path, 'r')
        return json.loads(f.read())








