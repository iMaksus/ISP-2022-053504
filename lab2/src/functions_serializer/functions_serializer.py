import sys
import inspect
import imp
from types import CodeType, FunctionType, ModuleType, WrapperDescriptorType, MappingProxyType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType


def _select_globals_func(globals : dict, func : FunctionType):
    actual_globals = {}
    for k, v in globals.items():
        if k in func.__code__.co_names:
            actual_globals.update({k: v})
    actual_globals.update(_select_subglobals_func(func, func.__code__))
    return actual_globals

def _select_subglobals_func(func : FunctionType, code : CodeType):
    actual_globals = {}
    for item in code.co_consts:
        if type(item) == CodeType:
            for k, v in func.__globals__.items():
                if k in item.co_names:
                    actual_globals.update({k: v})
            actual_globals.update(_select_subglobals_func(func, item))
    return actual_globals


def _select_fields_class(_class):
    fields = {}
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


def _is_module_builtin(name : str):
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


def _select_members_module(module : ModuleType) -> dict:
    module_members = {}
    for k, v in dict(inspect.getmembers(module)).items():
        if not k.startswith("__"):
            module_members.update({k:v})
    return module_members


def _select_attrs_module(module : ModuleType) -> dict:
    if _is_module_builtin(module.__name__):
        return None
    else:
        return _select_members_module(module)