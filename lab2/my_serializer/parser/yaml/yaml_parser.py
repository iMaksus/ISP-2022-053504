import inspect
import imp
import re
import yaml
from types import FunctionType, CodeType
from .dto_parser_yaml import DTO_TYPES, DTO_FIELDS_CLASS, DTO_FIELDS_CODE, DTO_FIELDS_FUNC, DTO_FIELDS_MODULE, DTO_FIELDS_OBJ
from my_serializer.custom_functions import _turn_list_to_tuple


class YamlParser():
    __DTO_TYPES = DTO_TYPES()
    __DTO_FIELDS_CODE = DTO_FIELDS_CODE()
    __DTO_FIELDS_FUNC = DTO_FIELDS_FUNC()
    __DTO_FIELDS_CLASS = DTO_FIELDS_CLASS()
    __DTO_FIELDS_OBJ = DTO_FIELDS_OBJ()
    __DTO_FIELDS_MODULE = DTO_FIELDS_MODULE()


    def __init__(self):
        super().__init__()


    # converts YAML file to Python object
    def load(self, file_path : str) -> any:
        with open(file_path, 'r') as f:
            _str = f.read()
            obj = yaml.full_load(_str)
            return self._parse(obj)


    # converts YAML string to Python object
    def loads(self, _str : str) -> any:
        obj = yaml.full_load(_str)
        return self._parse(obj)


    def _parse_primitive(self, obj):
        return obj


    def _parse_tuple_list(self, obj):
        _list = []
        for item in obj:
            _list.append(self._parse(item))
        if type(obj) is tuple:
            return _turn_list_to_tuple(_list)
        return _list


    def _parse_dict(self, obj : dict):
        _dict = {}
        for k,v in obj.items():
            _dict.update({k:self._parse(v)})
        return _dict


    def _parse_func(self, obj):
        _func = None
        func_name = obj[self.__DTO_FIELDS_FUNC.name]
        func_globals = self._parse(obj[self.__DTO_FIELDS_FUNC.globals])
        func_defaults = self._parse(obj[self.__DTO_FIELDS_FUNC.defaults])
        func_closure = self._parse(obj[self.__DTO_FIELDS_FUNC.closure])
        func_docs = obj[self.__DTO_FIELDS_FUNC.docs]
        func_code = self._parse(obj[self.__DTO_FIELDS_FUNC.code])
        _func = FunctionType(func_code, func_globals, func_name, func_defaults, func_closure)
        _func.__globals__["__builtins__"] = __import__("builtins")
        _func.__setattr__("__doc__", func_docs)
        return _func


    def _parse_code(self, obj):
        _code = None
        _code = CodeType(
            obj[self.__DTO_FIELDS_CODE.co_argcount],
            obj[self.__DTO_FIELDS_CODE.co_posonlyargcount],
            obj[self.__DTO_FIELDS_CODE.co_kwonlyargcount],
            obj[self.__DTO_FIELDS_CODE.co_nlocals],
            obj[self.__DTO_FIELDS_CODE.co_stacksize],
            obj[self.__DTO_FIELDS_CODE.co_flags],
            obj[self.__DTO_FIELDS_CODE.co_code],
            self._parse(obj[self.__DTO_FIELDS_CODE.co_consts]),
            obj[self.__DTO_FIELDS_CODE.co_names],
            obj[self.__DTO_FIELDS_CODE.co_varnames],
            obj[self.__DTO_FIELDS_CODE.co_filename],
            obj[self.__DTO_FIELDS_CODE.co_name],
            obj[self.__DTO_FIELDS_CODE.co_firstlineno],
            obj[self.__DTO_FIELDS_CODE.co_lnotab],
            obj[self.__DTO_FIELDS_CODE.co_freevars],
            obj[self.__DTO_FIELDS_CODE.co_cellvars]
        )
        return _code


    def _parse_class(self, obj):
        _class = None
        class_name = obj[self.__DTO_FIELDS_CLASS.name]
        class_fields = self._parse(obj[self.__DTO_FIELDS_CLASS.fields])
        class_bases = (object,)
        if "__bases__" in class_fields:
            class_bases = tuple(class_fields["__bases__"])
        _class = type(class_name, class_bases, class_fields)
        return _class


    def _parse_obj(self, obj):
        _obj = None
        class_obj = self._parse(obj[self.__DTO_FIELDS_OBJ.obj_class])
        obj_dict = self._parse(obj[self.__DTO_FIELDS_OBJ.fields])
        obj_init = class_obj.__init__
        if inspect.isfunction(obj_init):
            if obj_init.__class__.__name__ == "function":
                delattr(class_obj, "__init__")
        _obj = class_obj()
        _obj.__init__ = obj_init
        _obj.__dict__ = obj_dict
        return _obj


    def _parse_module(self, obj):
        _module = None
        module_name = obj[self.__DTO_FIELDS_MODULE.name]
        module_attrs = obj[self.__DTO_FIELDS_MODULE.attrs]
        if module_attrs is None:
            _module = __import__(module_name)
        else:
            _module = imp.new_module(module_name)
            for field in module_attrs.items():
                setattr(_module,field[0],field[1])
        return _module


    def _parse(self, obj):
        if type(obj) in (int, float, str, bool) or obj is None:
            return self._parse_primitive(obj)
        elif type(obj) in (tuple, list):
            return self._parse_tuple_list(obj)
        elif not "DTO_TYPE" in obj.keys():
            return self._parse_dict(obj)
        else:
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
