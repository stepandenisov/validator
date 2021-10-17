import argparse
import json
import logging
import re

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('validator')

PATTERN_DCT = {
    "telephone": r'[+]\d-[(]\d{3}[)]-\d{3}-\d{2}-\d{2}',
    "weight": r'\d{2}',
    "inn": r'\d{12}',
    "passport_series": r'\d{2} \d{2}',
    "occupation": r'[А-Яа-яЁё ]+?',
    "age": r'\d{2}',
    "political_views": r'[А-Яа-яЁё ]+?',
    "worldview": r'[А-Яа-яЁё ]+?',
    "address": r'[А-Яа-яЁё0-9- .]+? \d+?'
}

parser = argparse.ArgumentParser()
parser.add_argument("input", help='File to validate')
parser.add_argument("output", help='File to write validate data in')
args = parser.parse_args()


class Reader:
    """
    Объект класса Reader репрезентует класс для записи из текстового файла.

    Он выполняет чтение данных из файла с последующим хранением этих данных
    в качестве свойства __data.
    """
    def __init__(self) -> None:
        """
        Инициализирует экзмепляр класса Reader.

        Attributes
        ----------
            __data: list
                свойство класса, которое хранит данные, прочитанные
                из файла, в виде списка.
        """
        self.__data = []

    @property
    def data(self) -> list:
        """
        Геттер класса Reader, возвращающий свойство __data.

        Returns
        -------
            list:
                Возвращает список данных, хранимых в __data.
        """
        return self.__data

    @data.setter
    def data(self, value: list) -> None:
        """
        Сеттер класса Reader, присваивает значение value свойству __data.
        """
        self.__data = value

    def read_json(self, path: str) -> None:
        """
        Выполняет чтение из файла с путём path с последующим занесением
        этих данных в свойство __data.

        Parameters
        ----------
            path : str
                Строка с адресом файла.
        """
        f = open(path, 'r')
        self.__data = json.loads(f.read())


class Validator:
    """
    Объект класса Validator репрезентует класс для валидации данных.

    Он выполняет валидацию данных, хранимых в виде объекта класса Reader,
    с помощью регулярных выражений по заданному шаблонному словарю.
    """
    def __init__(self, readers: Reader, pattern_dct: dict) -> None:
        """
        Инициализирует экзмепляр класса Reader.

        Attributes
        ----------
            invalid_count: int
                свойство, отвечающее за количество некорректных записей
            valid_count: int
                свойство, отвечающее за количество корректных записей
            reader: Reader
                свойство, которе хранит данные для обработки
            pattern_dct: dict
                своство, которое хранит шаблон словаря, ключи которого
                совпадают с ключами в словаре входных данных, а значения - регулярные
                выражения, проверяющие валидность этих данных.
            errors_count: dict
                свойство, которое хранит словарь для подсчёта количества
                ошибок по конкретным ключам.
        Parameters
        ----------
            readers : Reader
                Свойство типа Reader, которое хранит входные данные
            pattern_dct : dict
                Свойство типа dict, которе хранит шаблонный словарь для обработки.
        """
        self.__invalid_count = 0
        self.__valid_count = 0
        self.reader = readers
        self.pattern_dct = pattern_dct
        self.__errors_count = {key: 0 for key in self.pattern_dct}

    @property
    def invalid_count(self) -> int:
        """
        Геттер класса Validator, возвращающий свойство __invalid_count.

        Returns
        -------
            int:
                Возвращает количество некорректных записей.
        """
        return self.__invalid_count

    @property
    def valid_count(self) -> int:
        """
        Геттер класса Validator, возвращающий свойство __valid_count.

        Returns
        -------
            int:
                Возвращает количество корректных записей.
        """
        return self.__valid_count

    @property
    def errors_count(self) -> dict:
        """
        Геттер класса Validator, возвращающий свойство __errors_count.

        Returns
        -------
            dict:
                Возвращает словарь, который хранит число невалидных записей по типам ошибок.
        """
        return self.__errors_count

    def validate(self) -> list:
        """
        Выполняет валидацию данных с отслеживанием прогресса.

        Для каждого словаря в списке входных данных выполняет алгортим проверки
        на корректность выражения, сравнивая это выражение с шаблонным выражением
        из pattern_dct. В случае корректности инкрементирует число валидных записей.
        В противном случае, инкрементирует число некорректных записей.

        Returns
        -------
            dict:
                Возвращает список валидных данных.
        """
        result_dct = []
        for dct in tqdm(self.reader.data):
            flag = False
            for key in dct:
                if not re.match(self.pattern_dct[key], str(dct[key])):
                    self.errors_count[key] += 1
                    if not flag:
                        self.__invalid_count += 1
                        flag = True
            if not flag:
                result_dct.append(dct)
                self.__valid_count += 1
        return result_dct


reader = Reader()
reader.read_json(args.input)
validator = Validator(reader, PATTERN_DCT)
logger.info("Validating...")
result = validator.validate()
with open(args.output, 'w') as outfile:
    logger.info(f"Writing to {args.output}...")
    outfile.write(json.dumps(result, ensure_ascii=False, indent=4))
logger.info("Done")
logger.info(f'Count of correct data: {validator.valid_count}\n')
logger.info(f'Count of incorrect data: {validator.invalid_count}')
for k in validator.errors_count:
    logger.info(f'Errors in \"{k}\": {validator.errors_count[k]}')
