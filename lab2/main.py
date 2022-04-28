from src.serializer import JsonSerializer, TomlSerializer, YamlSerializer
from src.parser import JsonParser, TomlParser, YamlParser
import math

st = "helllo"

test_bytes = "Hello \xf0\x9f\x8d\x95"
test_list = [5, "3", "\xf0\x9f\x8d\x95", True, test_bytes, None, None]
dict2 = {"go":"55", "skyrim":"legendary"}
dict1 = {"mercedes" : 5, "bmw" : False}
test_dict = {"cannondale": 99, "salamaleykum" : "dict1", "5": "hello"}
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

def my_first_func(y = 7):
    print(test_tuple)
    print(opi)
    def hello():
        print(f"Hello world!!!{opi}")
    # y = 3
    return hello()

def closure228(v):
    def insome():
        return v
    print(opi)

    return insome

def test_func(t, n=5):
    """This is docstring of some function"""
    # test_tuple = (3, 6, "hello")
    t = 23
    # y = math.sin(4 * opi * t)
    print("Hello")
    # print(y)

    def test_func2(_dict):
        y = 8
        return _dict.keys()
    return test_func2(test_dict)


class ff():
    def __init__(self, t):
        self.oo = t
    def printing(t):
        print(t)
        # self.ii = 9


class TestClass():
    some_bool_value = True
    class_value = 18
    c = 10.2

    def __init__(self, a: int, b: int = 2):
        self.c += (a+b)

    def simple_func(self, arg1):
        """Aboba"""
        t = 6
        def _abobus(arg2):
            i = 7
            def _cringe():
                return math.pi ** 2 * self.c
            return math.sin(arg1 * arg2 * opi * t * i * _cringe())
        return _abobus(6)


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
        simple_func(5)



json_ser = JsonSerializer()
toml_ser = TomlSerializer()
yaml_ser = YamlSerializer()

_string_json = json_ser.dumps(TestClass)
# _string_toml = toml_ser.dumps(TestClass(2))
_string_yaml = yaml_ser.dumps(TestClass)

open('data.json', 'w').write(_string_json)
# open('data.toml', 'w').write(_string_toml)
open('data.yaml', 'w').write(_string_yaml)


_str_json = open('data.json', 'r').read()
# _str_toml = open('data.toml', 'r').read()
_str_yaml = open('data.yaml', 'r').read()

json_pars = JsonParser()
# toml_pars = TomlParser()
yaml_pars = YamlParser()

obj_json = json_pars.loads(_str_json)
# obj_toml = toml_pars.loads(_str_toml)
obj_yaml = yaml_pars.loads(_str_yaml)


print(obj_json(5).simple_func(2))
# print(obj_toml.simple_func(5))
print(obj_yaml(5).simple_func(2))

# print(obj.count())

# json_ser2 = JsonSerializer()
# _string_json2 = json_ser2.dumps(MaksimClass)
# open('data.json', 'w').write(_string_json2)
# _str_json2 = open('data.json', 'r').read()
# json_pars2 = JsonParser()
# obj_json2 = json_pars2.loads(_str_json2)
# ob3 = obj_json2(2)
# ob3.printing()


def main():
    pass


if __name__ == "__main__":
    main()
