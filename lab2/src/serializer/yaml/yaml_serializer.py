import sys
import inspect
import imp
import yaml
from types import CodeType, FunctionType, ModuleType, WrapperDescriptorType, MappingProxyType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType

from src.base_serializator import BaseSerializator
from .dto_serialize_yaml import DTO_LIST, DTO_BYTES, DTO_FUNC, DTO_CODE, DTO_CLASS, DTO_OBJ, DTO_MODULE
from src.custom_functions import _select_globals_func, _select_fields_class, _select_attrs_module


class YamlSerializer(BaseSerializator):
    __str = ""


    def __init__(self):
        super().__init__()


    # converts Python object to TOML file
    def dump(self, obj : any, stream):
        yaml.dump(obj, stream)


    # converts Python object to TOML string
    def dumps(self, obj : any):
        self._serialize(obj)
        return self.__str


    # converts TOML file to Python object
    def load():
        pass


    # converts TOML string to Python object
    def loads():
        pass


    def _construct_primitive(self, obj):
        return obj


    def _construct_tuple_list(self, _list):
        new_list = []
        for item in _list:
            new_list.append(self._construct(item))
        return new_list


    def _construct_dict(self, _dict : dict):
        new_dict = {}
        for k,v in _dict.items():
            new_dict.update({k:self._construct(v)})
        return new_dict


    def _construct_bytes(self, obj):
        return obj


    def _construct_func(self, _func) -> dict:
        dto_code = self._construct(_func.__code__)
        dto_func = DTO_FUNC(
            DTO_TYPE = "func",
            name = self._construct(_func.__name__),
            globals = self._construct(_select_globals_func(_func.__globals__, _func)),
            code = dto_code,
            defaults = _func.__defaults__,
            closure = _func.__closure__,
            docs = _func.__doc__
        )
        dict_func = dto_func.dict()
        return dto_func.dict()


    def _construct_code(self, _code) -> dict:
        dto_code = DTO_CODE(
            DTO_TYPE = "code",
            co_argcount = _code.co_argcount,
            co_posonlyargcount = _code.co_posonlyargcount,
            co_kwonlyargcount = _code.co_kwonlyargcount,
            co_nlocals = _code.co_nlocals,
            co_stacksize = _code.co_stacksize,
            co_flags = _code.co_flags,
            co_code = _code.co_code,
            co_consts = self._construct(_code.co_consts),
            co_names = _code.co_names,
            co_varnames = _code.co_varnames,
            co_filename = _code.co_filename,
            co_name = _code.co_name,
            co_firstlineno = _code.co_firstlineno,
            co_lnotab = _code.co_lnotab,
            co_freevars = _code.co_freevars,
            co_cellvars = _code.co_cellvars
        )
        return dto_code.dict()


    def _construct_class(self, obj):
        dto_class = DTO_CLASS(
            DTO_TYPE = "class",
            name = obj.__name__,
            fields = self._construct(_select_fields_class(obj))
        )
        return dto_class.dict()


    def _construct_obj(self, obj):
        dto_obj = DTO_OBJ(
            DTO_TYPE = "obj",
            fields = self._construct(obj.__dict__),
            obj_class = self._construct_class(obj.__class__)
        )
        return dto_obj.dict()


    def _construct_module(self, obj):
        module_attrs = self._construct(_select_attrs_module(obj))
        dto_module = DTO_MODULE(
            DTO_TYPE = "module",
            name = obj.__name__,
            attrs = module_attrs
        )
        return dto_module.dict()


    def _construct_default(self, obj):
        return obj


    def _construct(self, obj):
        """Change any type to dict or list type for serializing through yaml"""
        _type = type(obj)
        if _type in (int, float, bool, str) or obj is None:
            return self._construct_primitive(obj)
        elif _type is bytes:
            return self._construct_bytes(obj)
        elif _type in (tuple, list):
            return self._construct_tuple_list(obj)
        elif _type is dict:
            return self._construct_dict(obj)
        elif inspect.isfunction(obj):
            return self._construct_func(obj)
        elif _type == CodeType:
            return self._construct_code(obj)
        elif inspect.isclass(obj):
            return self._construct_class(obj)
        elif inspect.ismodule(obj):
            return self._construct_module(obj)
        elif isinstance(obj, object):
            return self._construct_obj(obj)
        else:
            return self._construct_default(obj)


    def _serialize(self, obj):
        new_obj = self._construct(obj)
        self.__str += yaml.dump(new_obj)