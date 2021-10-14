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
            __data - свойство класса, которое хранит данные, прочитанные
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
            invalid_count - свойство, отвечающее за количество некорректных записей
            valid_count - свойство, отвечающее за количество корректных записей
            reader - свойство, которе хранит данные для обработки
            pattern_dct - своство, которое хранит шаблон словаря, ключи которого
            совпадают с ключами в словаре входных данных, а значения - регулярные
            выражения, проверяющие валидность этих данных.
            errors_count - свойство, которое хранит словарь для подсчёта количества
            ошибок по конкретным ключам.
        Parameters
        ----------
            readers : Reader
                Свойство типа Reader, которое хранит входные данные
            pattern_dct : dict
                Свойство типа dict, которе хранит шаблонный словарь для обработки.
        """
        self.invalid_count = 0
        self.valid_count = 0
        self.reader = readers
        self.pattern_dct = pattern_dct
        self.errors_count = {key: 0 for key in self.pattern_dct}

    def validate(self) -> None:
        """
        Выполняет валидацию данных.

        Для каждого словаря в списке входных данных выполняет алгортим проверки
        на корректность выражения, сравнивая это выражение с шаблонным выражением
        из pattern_dct. В случае корректности инкрементирует число валидных записей.
        В противном случае, инкрементирует число некорректных записей.
        """
        for element in self.reader.data:
            data_keys = list(element)
            flag = False
            for key in data_keys:
                if not re.match(self.pattern_dct[key], str(element[key])):
                    self.errors_count[key] += 1
                    if not flag:
                        self.invalid_count += 1
                        flag = True
            if not flag:
                self.valid_count += 1


reader = Reader()
reader.read_json("C:\\Users\\Stepan\\Downloads\\86.txt")
validator = Validator(reader, PATTERN_DCT)
validator.validate()
