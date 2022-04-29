import sys
import inspect
import imp
import toml
from types import CodeType, ModuleType

from .dto_serialize_toml import DTO_BYTES, DTO_FUNC, DTO_CODE, DTO_CLASS, DTO_OBJ, DTO_MODULE
from my_serializer.custom_functions import _select_globals_func, _select_fields_class, _select_attrs_module

class TomlSerializer():
    __str = ""


    def __init__(self):
        super().__init__()


    # converts Python object to TOML file
    def dump(self, obj : any, file_path : str):
        with open(file_path, 'w') as f:
            self._serialize(obj)
            f.write(self.__str)


    # converts Python object to TOML string
    def dumps(self, obj : any) -> str:
        self._serialize(obj)
        return self.__str


    def _construct_primitive(self, obj):
        if obj is None:
            return "TYPE=NONE"
        return obj


    def _construct_default(self, obj):
        return obj


    def _construct_dict(self, _dict: dict):
        new_dict = {}
        for k,v in _dict.items():
            new_dict.update({k: self._construct(v)})
        return new_dict


    def _construct_list_tuple(self, _list) -> dict:
        if _list == [] or _list == None:
            return {}
        list_dict = {}
        list_dict.update({"DTO_TYPE":"list"})
        for i, val in enumerate(_list):
            list_dict.update({f"ITEM_{i}":self._construct(val)})
        return list_dict


    def _construct_bytes(self, obj):
        dto_bytes = DTO_BYTES(
            DTO_TYPE="bytes",
            field=obj.hex()
        )
        return dto_bytes.dict()


    def _construct_func(self, _func) -> dict:
        dto_code = self._construct(_func.__code__)
        dto_func = DTO_FUNC(
            DTO_TYPE = "func",
            name = self._construct(_func.__name__),
            globals = self._construct(_select_globals_func(_func.__globals__, _func)),
            code = dto_code,
            defaults = self._construct_list_tuple(_func.__defaults__),
            closure = self._construct_list_tuple(_func.__closure__),
            docs = _func.__doc__ 
        )
        # dict_func = dto_func.dict()
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
            co_code = self._construct(_code.co_code),
            co_consts = self._construct(_code.co_consts),
            co_names = self._construct(_code.co_names),
            co_varnames = self._construct(_code.co_varnames),
            co_filename = _code.co_filename,
            co_name = _code.co_name,
            co_firstlineno = _code.co_firstlineno,
            co_lnotab = self._construct(_code.co_lnotab),
            co_freevars = self._construct(_code.co_freevars),
            co_cellvars = self._construct(_code.co_cellvars)
        )
        return dto_code.dict()


    def _construct_class(self, _class) -> dict:
        dto_class = DTO_CLASS(
            DTO_TYPE = "class",
            name = _class.__name__,
            fields = self._construct(_select_fields_class(_class))
        )
        # class_dict = dto_class.dict()
        return dto_class.dict()



    def _construct_obj(self, _obj) -> dict:
        dto_obj = DTO_OBJ(
            DTO_TYPE = "obj",
            fields = self._construct(_obj.__dict__),
            obj_class = self._construct_class(_obj.__class__)
        )
        return dto_obj.dict()


    def _construct_module(self, _module : ModuleType):
        module_attrs = self._construct(_select_attrs_module(_module))
        if module_attrs == "TYPE=NONE":
            module_attrs = None
        dto_module = DTO_MODULE(
            DTO_TYPE = "module",
            name = _module.__name__,
            attrs = module_attrs
        )
        return self._construct_dict(dto_module.dict())


    def _construct(self, obj):
        """Change any type to dict type for serializing through toml"""
        _type = type(obj)
        if _type in (int, float, bool, str) or obj is None:
            return self._construct_primitive(obj)
        elif _type is bytes:
            return self._construct_bytes(obj)
        elif _type is dict:
            return self._construct_dict(obj)
        elif _type in (list, tuple):
            return self._construct_list_tuple(obj)
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
        _type = type(obj)
        if _type in (int,float,bool,str,bytes) or obj is None:
            if _type in (int,float):
                self.__str += toml.dumps({"TYPE_NUMBER":obj})
            elif _type is bool:
                self.__str += toml.dumps({"TYPE_BOOL":obj})
            elif _type is str:
                self.__str += toml.dumps({"TYPE_STR":obj})
            elif _type is bytes:
                self.__str += toml.dumps({"TYPE_BYTES":obj})
            elif obj is None:
                self.__str += toml.dumps({"TYPE=NONE"})
        else:
            obj_dict = self._construct(obj)
            self.__str += toml.dumps(obj_dict)