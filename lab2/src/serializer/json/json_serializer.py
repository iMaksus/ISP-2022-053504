import inspect
import sys
from types import CodeType, ModuleType, WrapperDescriptorType, MappingProxyType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType
from src.base_serializator import BaseSerializator
from src.dto import DTO_func, DTO_code_func, DTO_class, DTO_obj


class JsonSerializer(BaseSerializator):
    __str = ""
    __obj = None

    def __init__(self, obj: any) -> None:
        self.__obj = obj
        #self.__globals = _globals
        # print(locals())

    # converts Python object to JSON file
    def dump():
        pass

    # converts Python object to JSON string
    def dumps(self) -> str:
        self._serialize(self.__obj)
        return self.__str

    # converts JSON file to Python object
    def load():
        pass

    # converts JSON string to Python object
    def loads():
        pass

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
            self._put(f'"{obj.hex()}"')
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

    # need to work
    def _serialize_dict(self, dict: dict):
        self._put('{')
        for k, v in dict.items():
            if not k is list(dict.keys())[0]:
                self._put(',')
            self._serialize(str(k))
            self._put(':')
            self._serialize(v)
        self._put('}')

    def _select_globals_func(self, globals : dict, code_names : tuple):
        actual_globals = {}
        for name in code_names:
            for k, v in globals.items():
                if name == k: actual_globals[k] = v
        return actual_globals
        
    def _construct_code_func(self, code) -> dict:
        dto_code_func = DTO_code_func(
            TYPE = "func code",
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

    def _serialize_code_func(self, obj):
        self._serialize(self._construct_code_func(obj))
    
    def _serialize_func(self, func):
        dto_code_func = self._construct_code_func(func.__code__)
        dto_func = DTO_func(
            TYPE = "func",
            name = func.__name__,
            globals = self._select_globals_func(func.__globals__, dto_code_func["co_names"]),
            code = dto_code_func,
            defaults = func.__defaults__,
            closure = func.__closure__
        )
        self._serialize(dto_func.dict())

    def _select_fields_class(self, _class):
        fields = dict()
        if _class == type:
            fields["__bases__"] = []
        else:
            for attr_name, attr_value in inspect.getmembers(_class):
                if not type(attr_value) in (
                    WrapperDescriptorType,
                    MappingProxyType,
                    MethodDescriptorType,
                    BuiltinFunctionType,
                    GetSetDescriptorType
                ) and not attr_name in (
                    '__basicsize__',
                    '__dictoffset__',
                    '__flags__',
                    '__itemsize__',
                    '__qualname__',
                    '__text_signature__',
                    '__weakrefoffset__',
                    '__name__',
                    '__base__',
                    '__mro__',
                    '__class__'
                ):
                    fields[attr_name] = attr_value
        return fields


    def _construct_class(self, _class) -> dict:
        dto_class = DTO_class(
            TYPE = "class",
            name = _class.__name__,
            fields = self._select_fields_class(_class)
        )
        return dto_class.dict()

    def _serialize_class(self, _class):
        self._serialize(self._construct_class(_class))

    def _serialize_obj(self, obj):
        dto_obj = DTO_obj(
            TYPE = "object",
            fields = obj.__dict__,
            obj_class = self._construct_class(obj.__class__)
        )
        self._serialize(dto_obj.dict())
        
    def _serialize_module(self, module):
        pass
        # self._parse_module(module)        

    # def _parse_module(self, module):
    #     new_module = ModuleType(module.__name__, module.__doc__)
    #     new_module.__dict__.update(module.__dict__)
    #     sys.modules[module.__name__] = new_module

    #     wow_module = __import__(module.__name__, globals=None, locals=None, fromlist=True)

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
            self._serialize_code_func(obj)
        elif inspect.isclass(obj):
            self._serialize_class(obj)
        elif inspect.ismodule(obj):
            self._serialize_module(obj)
        elif isinstance(obj, object):
            self._serialize_obj(obj)
        else:
            self._serialize_default(obj)
