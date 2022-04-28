import sys
import inspect
import imp
from types import CodeType, ModuleType

from src.base_serializator import BaseSerializator
from .dto_serialize_json import DTO_FUNC, DTO_CODE, DTO_CLASS, DTO_OBJ, DTO_MODULE
from src.custom_functions import _select_globals_func, _select_fields_class, _select_attrs_module


class JsonSerializer():
    __str = ""


    def __init__(self) -> None:
        super().__init__()


    # converts Python object to JSON file
    def dump():
        pass


    # converts Python object to JSON string
    def dumps(self, obj : any) -> str:
        self._serialize(obj)
        return self.__str


    def _put(self, s: str):
        self.__str += s


    def _serialize_primitive(self, obj: any):
        _type = type(obj)
        if _type in (int, float):
            self._put(f'{obj}')
        elif _type == bool:
            self._put('true') if obj else self._put('false')
        elif _type == str:
            self._put(f'"{obj}"')
        elif _type == bytes:
            self._put('{')
            self._put('"TYPE":"bytes",')
            self._put('"field":')
            decode = obj.hex()
            self._put(f'"{decode}"')
            self._put('}')
        elif obj is None:
            # self._put('{}')
            self._put('null')


    def _serialize_tuple_list(self, obj):
        self._put('[')
        for item in obj:
            if not item is obj[0]:
                self._put(',')
            self._serialize(item)
        self._put(']')


    def _serialize_dict(self, dict: dict):
        self._put('{')
        for k, v in dict.items():
            if not k is list(dict.keys())[0]:
                self._put(',')
            self._serialize(str(k))
            self._put(':')
            self._serialize(v)
        self._put('}')
                

    def _construct_code(self, code) -> dict:
        dto_code_func = DTO_CODE(
            TYPE = "code",
            co_argcount = code.co_argcount,
            co_posonlyargcount = code.co_posonlyargcount,
            co_kwonlyargcount = code.co_kwonlyargcount,
            co_nlocals = code.co_nlocals,
            co_stacksize = code.co_stacksize,
            co_flags = code.co_flags,
            co_code = code.co_code,
            co_consts = code.co_consts,
            co_names = code.co_names,
            co_varnames = code.co_varnames,
            co_filename = code.co_filename,
            co_name = code.co_name,
            co_firstlineno = code.co_firstlineno,
            co_lnotab = code.co_lnotab,
            co_freevars = code.co_freevars,
            co_cellvars = code.co_cellvars
        )
        return dto_code_func.dict()


    def _serialize_code(self, obj):
        self._serialize(self._construct_code(obj))
    

    def _serialize_func(self, func):
        dto_code_func = self._construct_code(func.__code__)
        dto_func = DTO_FUNC(
            TYPE = "func",
            name = func.__name__,
            globals = _select_globals_func(func.__globals__, func),
            code = dto_code_func,
            defaults = func.__defaults__,
            closure = func.__closure__,
            docs = func.__doc__
        )
        self._serialize(dto_func.dict())


    def _construct_class(self, _class) -> dict:
        dto_class = DTO_CLASS(
            TYPE = "class",
            name = _class.__name__,
            fields = _select_fields_class(_class)
        )
        return dto_class.dict()


    def _serialize_class(self, _class):
        self._serialize(self._construct_class(_class))


    def _serialize_obj(self, obj):
        dto_obj = DTO_OBJ(
            TYPE = "obj",
            fields = obj.__dict__,
            obj_class = self._construct_class(obj.__class__)
        )
        self._serialize(dto_obj.dict())


    def _serialize_module(self, module : ModuleType):
        dto_module = DTO_MODULE(
            TYPE = "module",
            name = module.__name__,
            attrs = _select_attrs_module(module)
        )
        self._serialize(dto_module.dict())


    def _serialize_default(self, obj):
        self._put(f'"{str(obj)}"')


    # distributing types to function
    def _serialize(self, obj: any):
        _type = type(obj)
        if _type in (int, float, bool, str, bytes) or obj is None:
            self._serialize_primitive(obj)
        elif _type in (list, tuple):
            self._serialize_tuple_list(obj)
        elif _type is dict:
            self._serialize_dict(obj)
        elif inspect.isfunction(obj):
            self._serialize_func(obj)
        elif _type == CodeType:
            self._serialize_code(obj)
        elif inspect.isclass(obj):
            self._serialize_class(obj)
        elif inspect.ismodule(obj):
            self._serialize_module(obj)
        elif isinstance(obj, object):
            self._serialize_obj(obj)
        else:
            self._serialize_default(obj)
