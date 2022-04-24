import inspect
import sys
import imp
from types import CodeType, FunctionType, ModuleType, WrapperDescriptorType, MappingProxyType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType
from src.base_serializator import BaseSerializator
from src.dto import DTO_FUNC, DTO_CODE, DTO_CLASS, DTO_OBJ, DTO_MODULE


class JsonSerializer(BaseSerializator):
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
            self._put('{')
            self._put('"TYPE":"bytes",')
            self._put('"field":')
            decode = obj.hex()
            # decode = obj.decode("UTF-8")
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


    def _select_globals_func(self, globals : dict, func : FunctionType):
        actual_globals = {}
        for k, v in globals.items():
            if k in func.__code__.co_names:
                actual_globals.update({k: v})
        actual_globals.update(self._select_subglobals_func(func, func.__code__))
        return actual_globals
        

    def _select_subglobals_func(self, func : FunctionType, code : CodeType):
        actual_globals = {}
        for item in code.co_consts:
            if type(item) == CodeType:
                for k, v in func.__globals__.items():
                    if k in item.co_names:
                        actual_globals.update({k: v})
                actual_globals.update(self._select_subglobals_func(func, item))
        return actual_globals
                

    def _construct_code_func(self, code) -> dict:
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


    def _serialize_code_func(self, obj):
        self._serialize(self._construct_code_func(obj))
    

    def _serialize_func(self, func):
        dto_code_func = self._construct_code_func(func.__code__)
        dto_func = DTO_FUNC(
            TYPE = "func",
            name = func.__name__,
            globals = self._select_globals_func(func.__globals__, func),
            code = dto_code_func,
            defaults = func.__defaults__,
            closure = func.__closure__,
            docs = func.__doc__
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
        dto_class = DTO_CLASS(
            TYPE = "class",
            name = _class.__name__,
            fields = self._select_fields_class(_class)
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


    def _is_module_builtin(self, name : str):
        python_libs_path = sys.path[2]
        print(python_libs_path)
        module_path = imp.find_module(name)[1]
        print(module_path)
        if name in sys.builtin_module_names:
            return True
        elif python_libs_path in module_path:
            return True
        elif 'site-packages' in module_path:
            return True
        return False


    def _select_members_module(self, module : ModuleType) -> dict:
        module_members = {}
        for k, v in dict(inspect.getmembers(module)).items():
            if not k.startswith("__"):
                module_members.update({k:v})
        return module_members


    def _select_attrs_module(self, module : ModuleType) -> dict:
        if self._is_module_builtin(module.__name__):
            return None
        else:
            return self._select_members_module(module)


    def _serialize_module(self, module : ModuleType):
        # members = inspect.getmembers(module)
        dto_module = DTO_MODULE(
            TYPE = "module",
            name = module.__name__,
            attrs = self._select_attrs_module(module)
        )
        self._serialize(dto_module.dict())
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
