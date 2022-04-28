from collections import OrderedDict
import inspect
import imp
import re
import toml
from types import FunctionType, CodeType
from src.base_serializator import BaseSerializator
from .dto_parser_toml import DTO_TYPES, DTO_FIELDS_BYTES, DTO_FIELDS_CLASS, DTO_FIELDS_CODE, DTO_FIELDS_FUNC, DTO_FIELDS_MODULE, DTO_FIELDS_OBJ


class TomlParser(BaseSerializator):
    __DTO_TYPES = DTO_TYPES()
    __DTO_FIELDS_BYTES = DTO_FIELDS_BYTES()
    __DTO_FIELDS_CODE = DTO_FIELDS_CODE()
    __DTO_FIELDS_FUNC = DTO_FIELDS_FUNC()
    __DTO_FIELDS_CLASS = DTO_FIELDS_CLASS()
    __DTO_FIELDS_OBJ = DTO_FIELDS_OBJ()
    __DTO_FIELDS_MODULE = DTO_FIELDS_MODULE()


    def __init__(self):
        super().__init__()


    # converts Python object to TOML file
    def dump():
        pass


    # converts Python object to TOML string
    def dumps():
        pass


    # converts TOML file to Python object
    def load():
        pass


    # converts TOML string to Python object
    def loads(self, _str : str):
        obj_dict = toml.loads(_str)
        return self._parse(obj_dict)


    def _parse_primitive(self, obj: dict):
        if obj == "TYPE=NONE":
            return None
        return obj


    def _parse_dict(self, dct: dict):
        _dict = {}
        for k,v in dct.items():
            _dict.update({k:self._parse(v)})
        return _dict


    def _parse_list(self, dct: dict):
        _list = []
        dct = OrderedDict(sorted(dct.items()))
        for k,v in dct.items():
            if k == "DTO_TYPE": continue
            value = self._parse(v)
            if type(value) is list:
                _list += self._parse(value)
            else:
                _list.append(value)
        return _list


    def _parse_bytes(self, dct: dict):
        bstring = dct[self.__DTO_FIELDS_BYTES.field]
        _bytes = bytes.fromhex(bstring)
        return _bytes


    def _parse_func(self, dct: dict):
        _func = None
        func_name = dct[self.__DTO_FIELDS_FUNC.name]
        func_globals = self._parse(dct[self.__DTO_FIELDS_FUNC.globals])
        func_defaults = tuple(self._parse(dct[self.__DTO_FIELDS_FUNC.defaults]))
        func_closure = tuple(self._parse(dct[self.__DTO_FIELDS_FUNC.closure]))
        func_docs = dct[self.__DTO_FIELDS_FUNC.docs] if self.__DTO_FIELDS_FUNC.docs in dct.keys() else ""
        func_code = self._parse(dct[self.__DTO_FIELDS_FUNC.code])
        _func = FunctionType(func_code, func_globals, func_name, func_defaults, func_closure)
        _func.__globals__["__builtins__"] = __import__("builtins")
        _func.__setattr__("__doc__", func_docs)
        return _func


    def _parse_code(self, dct: dict):
        _code = None
        _code = CodeType(
            self._parse(dct[self.__DTO_FIELDS_CODE.co_argcount]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_posonlyargcount]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_kwonlyargcount]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_nlocals]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_stacksize]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_flags]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_code]),
            tuple(self._parse(dct[self.__DTO_FIELDS_CODE.co_consts])),
            tuple(self._parse(dct[self.__DTO_FIELDS_CODE.co_names])),
            tuple(self._parse(dct[self.__DTO_FIELDS_CODE.co_varnames])),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_filename]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_name]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_firstlineno]),
            self._parse(dct[self.__DTO_FIELDS_CODE.co_lnotab]),
            tuple(self._parse(dct[self.__DTO_FIELDS_CODE.co_freevars])),
            tuple(self._parse(dct[self.__DTO_FIELDS_CODE.co_cellvars]))
        )
        return _code


    def _parse_class(self, dct: dict):
        _class = None
        class_name = dct[self.__DTO_FIELDS_CLASS.name]
        class_fields = self._parse(dct[self.__DTO_FIELDS_CLASS.fields])
        class_bases = (object,)
        if "__bases__" in class_fields:
            class_bases = tuple(class_fields["__bases__"])
        _class = type(class_name, class_bases, class_fields)
        return _class


    def _parse_obj(self, dct: dict):
        _obj = None
        class_obj = self._parse(dct[self.__DTO_FIELDS_OBJ.obj_class])
        obj_dict = self._parse(dct[self.__DTO_FIELDS_OBJ.fields])
        obj_init = class_obj.__init__
        if inspect.isfunction(obj_init):
            if obj_init.__class__.__name__ == "function":
                delattr(class_obj, "__init__")
        _obj = class_obj()
        _obj.__init__ = obj_init
        _obj.__dict__ = obj_dict
        return _obj


    def _parse_module(self, dct: dict):
        _module = None
        module_name = dct[self.__DTO_FIELDS_MODULE.name]
        module_attrs = dct[self.__DTO_FIELDS_MODULE.attrs]
        if module_attrs == "TYPE=NONE":
            _module = __import__(module_name)
        else:
            _module = imp.new_module(module_name)
            for field in module_attrs.items():
                setattr(_module,field[0],field[1])
        return _module

    
    def _parse(self, obj):
        if type(obj) in (int, float, str, bool, list) or obj is None:
            return self._parse_primitive(obj)
        elif not "DTO_TYPE" in obj.keys():
            return self._parse_dict(obj)
        else:
            if obj["DTO_TYPE"] == self.__DTO_TYPES.LIST:
                return self._parse_list(obj)
            if obj["DTO_TYPE"] == self.__DTO_TYPES.BYTES:
                return self._parse_bytes(obj)
            if obj["DTO_TYPE"] == self.__DTO_TYPES.FUNC:
                return self._parse_func(obj)
            elif obj["DTO_TYPE"] == self.__DTO_TYPES.CODE:
                return self._parse_code(obj)
            elif obj["DTO_TYPE"] == self.__DTO_TYPES.CLASS:
                return self._parse_class(obj)
            elif obj["DTO_TYPE"] == self.__DTO_TYPES.OBJ:
                return self._parse_obj(obj)
            elif obj["DTO_TYPE"] == self.__DTO_TYPES.MODULE:
                return self._parse_module(obj)