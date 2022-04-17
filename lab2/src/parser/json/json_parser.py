import inspect
from types import FunctionType, CodeType
from src.base_serializator import BaseSerializator
from src.dto import DTO_func, DTO_code_func, DTO_class, DTO_obj

# deserialize function using FunctionType :
# https://stackoverflow.com/questions/1253528/is-there-an-easy-way-to-pickle-a-python-function-or-otherwise-serialize-its-cod
# https://medium.com/@emlynoregan/serialising-all-the-functions-in-python-cd880a63b591

class JsonParser(BaseSerializator):
    __str = ""
    __obj = None

    def __init__(self):
        pass

    # converts Python object to JSON file
    def dump():
        pass

    # converts Python object to JSON string
    def dumps():
        pass

    # converts JSON file to Python object
    def load():
        pass

    # converts JSON string to Python object
    def loads(self, _str : str) -> any:
        self.__str = _str
        return self._parse(_str)

    def _parse_func(self, func: DTO_func):
        parse_func = FunctionType(
            self._parse_code_func(func.code), func.globals, func.name, func.defaults, func.closure)
        parse_func.__globals__["__builtins__"] = __import__("builtins")
        parse_func.__setattr__("__doc__", func.__doc__)
        print(parse_func(6))
        # self._parse_dict(parse_func.__code__)

    def _parse_code_func(self, code : dict):
        # print("-----code-----")
        # for k, v in dict(dir(code)).keys():
        #     print(f"{k} : {v}")
        # print("----------")
        # print(code[co_argcount])
        code_func = CodeType(
            code["co_argcount"],
            code["co_posonlyargcount"],
            code["co_kwonlyargcount"],
            code["co_nlocals"],
            code["co_stacksize"],
            code["co_flags"],
            code["co_code"],
            code["co_consts"],
            code["co_names"],
            code["co_varnames"],
            code["co_filename"],
            code["co_name"],
            code["co_firstlineno"],
            code["co_lnotab"],
            code["co_freevars"],
            code["co_cellvars"]
        )
        return code_func
        # print(code_func)
        # print(code)


    def _parse_class(self, _class):
        type(_class.__name__, _class.__bases__, {
            "__init__": _class.__init__,
            
        })
        new_class = type(_class.__name__, _class.__bases__, dict(_class.__dict__))
        obj = new_class()
        obj.welcome("matua")
        pass