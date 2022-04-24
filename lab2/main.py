from src.serializer import JsonSerializer
from src.parser import JsonParser
import math
import json
import test_module

st = "helllo"

test_bytes = "Hello \xf0\x9f\x8d\x95"
test_list = [5, "3", "\xf0\x9f\x8d\x95", True, test_bytes]
test_dict = {"cannondale": 99, "cube": test_list, "5": "hello"}
test_tuple = (6, "8", "\xf0\x9f\x8d\x95", test_dict, False)


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

    # def heel():
    #     return t * opi
    # return heel()


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
    # print(test_dict2.keys())
    ww = json.dumps(test_tuple)
    print(ww)

    def test_func2(_dict):
        y = 8
        return _dict.keys()
    return test_func2(test_dict)
# print(test_func.__code__)
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

opi = 2
class Meta228(type):
    s = 33
    # def __new__(cls, name, bases, dct):
    #     dct.update({"a": 228})
    #     print("something")
    #     return type(name, bases,dct)
    def simple_func(self, arg1):
        """Aboba"""
        t = 6
        def _h(arg2):
            i = 7
            def _hahahah():
                return math.pi ** 2
            return math.sin(arg1 * arg2 * opi * t * i * _hahahah())
        return _h(6)

class ccc(metaclass=Meta228):
    def pri(self):
        print(self.s)
    def omg_heissostrong(self):
        self.simple_func(5)

ff_obj = ff(8)
json_ser = JsonSerializer()
some_obj = TestClass(4)
_string = json_ser.dumps(some_obj)
open('data.json', 'w').write(_string)


_str_parse = open('data.json', 'r').read()
json_pars = JsonParser()
obj = json_pars.loads(_str_parse)

print(obj.count())

# test class 'ccc'
# obj_class = obj()
# print(type(obj_class))
# print(obj_class)
# print(obj_class.pri())
# print(obj_class.simple_func(5))

# with open('data.json', 'w') as write:
#     json.dump(f,write)

# with open('data.json', 'r') as j:
#     contents = json.loads(j.read())
#     print(contents)

def main():
    pass


if __name__ == "__main__":
    main()
