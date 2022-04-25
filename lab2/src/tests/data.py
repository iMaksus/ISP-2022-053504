import math

st = "helllo"

test_bytes = "Hello \xf0\x9f\x8d\x95"
test_list = [5, "3", "\xf0\x9f\x8d\x95", True, test_bytes, None, None]
dict2 = {"go":"55", "skyrim":"legendary"}
dict1 = {"mercedes" : 5, "bmw" : False}
test_dict = {"cannondale": 99, "salamaleykum" : "dict1", "5": "hello", "minecraft": test_list}
test_tuple = (6, "8", "\xf0\x9f\x8d\x95", test_dict, False)
tuple_1 = ["hello", "True"]
list_of_dicts = [dict1, dict2]


opi = 2
def simple_func(arg1):
    """Aboba"""
    t = 6
    def _h(arg2):
        i = 7
        def _hahahah():
            return math.pi ** 2
        return math.sin(arg1 * arg2 * opi * t * i * _hahahah())
    return _h(6)

def my_first_func():
    print(f"Hello world!!!{opi}")
    print(test_tuple)

def closure228(v):
    def insome():
        return v
    print(opi)

    return insome

def test_func(t, n=5):
    """This is docstring of some function"""
    test_tuple = (3, 6, "hello")
    t = 23
    y = math.sin(4 * opi * t)
    print("Hello")
    print(y)

    def test_func2(_dict):
        y = 8
        return _dict.keys()
    return test_func2(test_dict)


class test_parent():
    t = 5
class MetaMaksim(type):
    pass


class test_class(test_parent):
    def welcome(self, str):
        print(f"Hello {str}!")
    __y = 7
    def __init__(self):
        self.__y = 5
        print("matua535")


class ff():
    def __init__(self, t):
        self.oo = t
    def printing(t):
        print(t)
        # self.ii = 9


class MaksimClass(ff):
    t = 5
    def printing(t):
        print(t)
class emptycls():
    pass
class TestClass():
    some_bool_value = True
    class_value = 18
    c = 10.2

    def __init__(self, a: int, b: int = 2):
        self.c += (a+b)

    def count(self) -> int:
        return self.c/18


# class SimpleClass(type):
class SimpleClass(type):
    a = 10
    def __new__(cls, name, bases, attrs):
        attrs.update({"a": 20})
        print("hello")
        return type(name, bases, attrs)
    def simple_func(self, arg1):
        """Aboba"""
        t = 6
        def _abobus(arg2):
            i = 7
            def _cringe():
                return math.pi ** 2 * self.a
            return math.sin(arg1 * arg2 * opi * t * i * _cringe())
        return _abobus(6)


class AnotherClass(metaclass=SimpleClass):
    def pri(self):
        print(self.a)
    def omg_heissostrong(self):
        self.simple_func(5)