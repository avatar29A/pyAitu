class Helper:
    mode = ''

    @classmethod
    def all(cls):
        result = []

        for name in dir(cls):
            if not name.isupper():
                continue
            value = getattr(cls, name)
            if isinstance(value, ItemsList):
                result.append(value[0])
            else:
                result.append(value)
        return result


class HelperMode(Helper):
    SCREAMING_SNAKE_CASE = 'SCREAMING_SNAKE_CASE'
    lowerCamelCase = 'lowerCamelCase'
    CamelCase = 'CamelCase'
    snake_case = 'snake_case'
    lowercase = 'lowercase'

    @classmethod
    def all(cls):
        return [
            cls.SCREAMING_SNAKE_CASE,
            cls.lowerCamelCase,
            cls.CamelCase,
            cls.snake_case,
            cls.lowercase,
        ]

    @classmethod
    def _screaming_snake_case(cls, text):
        if text.isupper():
            return text
        result = ''
        for pos, symbol in enumerate(text):
            if symbol.isupper() and pos > 0:
                result += '_' + symbol
            else:
                result += symbol.upper()
        return result

    @classmethod
    def _snake_case(cls, text):
        if text.islower():
            return text
        return cls._screaming_snake_case(text).lower()

    @classmethod
    def _camel_case(cls, text, first_upper=False):
        result = ''
        need_upper = False
        for pos, symbol in enumerate(text):
            if symbol == '_' and pos > 0:
                need_upper = True
            else:
                if need_upper:
                    result += symbol.upper()
                else:
                    result += symbol.lower()
                need_upper = False
        if first_upper:
            result = result[0].upper() + result[1:]
        return result

    @classmethod
    def apply(cls, text, mode):
        if mode == cls.SCREAMING_SNAKE_CASE:
            return cls._screaming_snake_case(text)
        if mode == cls.snake_case:
            return cls._snake_case(text)
        if mode == cls.lowercase:
            return cls._snake_case(text).replace('_', '')
        if mode == cls.lowerCamelCase:
            return cls._camel_case(text)
        if mode == cls.CamelCase:
            return cls._camel_case(text, True)
        if callable(mode):
            return mode(text)
        return text


class Item:
    def __init__(self, value=None):
        self._value = value

    def __get__(self, instance, owner):
        return self._value

    def __set_name__(self, owner, name):
        if not name.isupper():
            raise NameError('Name for helper item must be in uppercase!')
        if not self._value:
            if hasattr(owner, 'mode'):
                self._value = HelperMode.apply(name, getattr(owner, 'mode'))


class ListItem(Item):
    def add(self, other):
        return self + other

    def __get__(self, instance, owner):
        return ItemsList(self._value)

    def __getitem__(self, item):
        return self._value

    __iadd__ = __add__ = __rand__ = __and__ = __ror__ = __or__ = add


class ItemsList(list):
    def __init__(self, *seq):
        super(ItemsList, self).__init__(map(str, seq))

    def add(self, other):
        self.extend(other)
        return self

    __iadd__ = __add__ = __rand__ = __and__ = __ror__ = __or__ = add
