import sys
import inspect
import imp
import toml
from types import CodeType, FunctionType, ModuleType, WrapperDescriptorType, MappingProxyType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType

from src.base_serializator import BaseSerializator
from .dto_serialize_toml import DTO_LIST, DTO_BYTES, DTO_FUNC, DTO_CODE, DTO_CLASS, DTO_OBJ, DTO_MODULE
from src.functions_serializer import _select_globals_func, _select_fields_class, _select_attrs_module

class TomlSerializer(BaseSerializator):
    __str = ""


    def __init__(self):
        super().__init__()


    # converts Python object to JSON file
    def dump():
        pass


    # converts Python object to JSON string
    def dumps(self, obj : any):
        self._serialize(obj)
        return self.__str


    # converts JSON file to Python object
    def load():
        pass


    # converts JSON string to Python object
    def loads():
        pass


    def _construct_primitive(self, obj):
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
            # return {"fields":None}
            # return None
        other_fields = {}
        i, k, j = 1, 1, 1
        dto_list = DTO_LIST(
            DTO_TYPE="list",
            TYPE_INT=[],
            TYPE_STR=[],
            TYPE_BOOL=[],
            TYPE_NONE=[])
        for item in _list:
            _type = type(item)
            if _type in (int, float):
                dto_list.TYPE_INT.append(item)
            elif _type is str:
                dto_list.TYPE_STR.append(item)
            elif _type is bool:
                dto_list.TYPE_BOOL.append(item)
            elif item == None:
                dto_list.TYPE_NONE.append(item)
            elif _type is dict:
                other_fields.update({f"TYPE_DICT_{i}": self._construct(item)})
                i+=1
            elif inspect.isfunction(item):
                other_fields.update({item.__name__: self._construct(item)})
            elif _type == CodeType:
                other_fields.update({"TYPE_CODE": self._construct(item)})
            elif inspect.isclass(item):
                other_fields.update({item.__name__: self._construct(item)})
            elif inspect.ismodule(item):
                other_fields.update({item.__name__: self._construct(item)})
            elif isinstance(item, object):
                other_fields.update({f"TYPE_OBJECT_{j}": self._construct(item)})
                j+=1
            else:
                other_fields.update({f"TYPE_OTHER_{k}": self._construct(item)})
                k+=1
        list_dict = dto_list.dict()
        list_dict.update(other_fields)
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
        class_dict = dto_class.dict()
        return dto_class.dict()



    def _construct_obj(self, _obj) -> dict:
        dto_obj = DTO_OBJ(
            DTO_TYPE = "obj",
            fields = self._construct(_obj.__dict__),
            obj_class = self._construct_class(_obj.__class__)
        )
        gg = dto_obj.dict()
        return dto_obj.dict()


    def _construct_module(self, _module : ModuleType):
        dto_module = DTO_MODULE(
            DTO_TYPE = "module",
            name = _module.__name__,
            attrs = self._construct(_select_attrs_module(_module))
        )
        hh = dto_module.dict()
        return dto_module.dict()


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
        if type(obj) in (int, float, bool, str, bytes) or obj is None:
            self.__str += toml.dumps({type(obj):obj})
        else:
            obj_dict = self._construct(obj)
            self.__str += toml.dumps(obj_dict)