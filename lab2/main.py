import math
import test_module
from src.serializer import JsonSerializer
from src.parser import JsonParser

test_bytes = "Hello \xf0\x9f\x8d\x95"
test_list = [5, "3", "\xf0\x9f\x8d\x95", True]
test_tuple = (6, "8", "\xf0\x9f\x8d\x95", False)
test_dict = {8: "cannondale", True: "cube", "5": 6}


opi = 4

gg = None
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
ff_obj = ff(8)
f = 6
json_ser = JsonSerializer(test_module)
_string = json_ser.dumps()
json_pars = JsonParser(_string)

open('data.json', 'w').write(_string)


def main():
    pass


if __name__ == "__main__":
    main()
