import inspect
import imp
import re
from types import FunctionType, CodeType
from .dto_parse_json import DTO_REGEX, DTO_TYPES
from src.base_serializator import BaseSerializator


# deserialize function using FunctionType :
# https://stackoverflow.com/questions/1253528/is-there-an-easy-way-to-pickle-a-python-function-or-otherwise-serialize-its-cod
# https://medium.com/@emlynoregan/serialising-all-the-functions-in-python-cd880a63b591


class JsonParser(BaseSerializator):
    __str = ""
    __divided = []
    __DTO_REGEX = DTO_REGEX()
    __DTO_TYPES = DTO_TYPES()


    def __init__(self):
        super().__init__()


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
    def loads(self, _str : str):
        self.__divided = self._divide_str(_str)
        return self._parse_first()


    def _get(self, type_to_skip : tuple):
        if len(self.__divided):
            if self.__divided[0][0] in type_to_skip:
                return self.__divided.pop(0)
        return ("", "")


    def _check_first(self):
        if len(self.__divided):
            return self.__divided[0]


    def _skip_key(self):
        self._get(self.__DTO_TYPES.COMMA)
        self._get(self.__DTO_TYPES.STR)
        self._get(self.__DTO_TYPES.COLON)


    def _divide_str(self, _str : str):
        # _str = r'{"GHell":"some val",[6,"hyyu"],"wooow":null,"woohoo":true}'
        divided = []
        while len(_str) > 0:
            for nameexp, regexp in self.__DTO_REGEX.dict().items():
                reg_chars = re.match(regexp, _str)
                if reg_chars == None:
                    continue
                elif reg_chars.start() != 0:
                    continue
                else:
                    _str = str(_str[reg_chars.end() - reg_chars.start():]).strip()
                    if nameexp == self.__DTO_TYPES.NULL:
                        divided.append((nameexp,None))
                    elif nameexp == self.__DTO_TYPES.STR:
                        str88 = reg_chars.group(0)
                        divided.append((nameexp, str88.replace('"', '')))
                    elif nameexp == self.__DTO_TYPES.NUMBER:
                        number = reg_chars.group(0)
                        __number = float(number) if '.' in number else int(number)
                        divided.append((nameexp, __number))
                    elif nameexp == self.__DTO_TYPES.BOOL:
                        __bool = True if reg_chars.group(0) == "true" else False
                        divided.append((nameexp, __bool))
                    else:
                        divided.append((nameexp,))
                        break
        divided.append((self.__DTO_TYPES.EOF,))
        return divided


    def _parse_primitive(self) -> any:
        if self._check_first()[0] == self.__DTO_TYPES.NUMBER:
            return self._get(self.__DTO_TYPES.NUMBER)[1]
        elif self._check_first()[0] == self.__DTO_TYPES.STR:
            return self._get(self.__DTO_TYPES.STR)[1]
        elif self._check_first()[0] == self.__DTO_TYPES.NULL:
            return self._get(self.__DTO_TYPES.NULL)[1]
        elif self._check_first()[0] == self.__DTO_TYPES.BOOL:
            return self._get(self.__DTO_TYPES.BOOL)[1]


    def _parse_dict(self):
        _dict = {}
        while True:
            key = self._get(self.__DTO_TYPES.STR)[1]
            self._get(self.__DTO_TYPES.COLON)
            value = self._parse()
            _dict.update({key: value})
            self._get(self.__DTO_TYPES.COMMA)
            if self._check_first()[0] == self.__DTO_TYPES.RBRACE:
                break
        self._get(self.__DTO_TYPES.RBRACE)
        return _dict


    def _parse_list(self):
        _list = []
        self._get(self.__DTO_TYPES.LBRACKET)
        if self._check_first()[0] == self.__DTO_TYPES.RBRACKET:
            self._get(self.__DTO_TYPES.RBRACKET)
            return []
        while True:
            item = self._parse()
            _list.append(item)
            self._get(self.__DTO_TYPES.COMMA)
            if self._check_first()[0] == self.__DTO_TYPES.RBRACKET:
                break
        self._get(self.__DTO_TYPES.RBRACKET)
        return _list


    def _parse_func(self):
        _func = None
        self._get(self.__DTO_TYPES.STR)
        self._get(self.__DTO_TYPES.COMMA)
        self._skip_key()
        func_name : str = self._get(self.__DTO_TYPES.STR)[1]
        self._skip_key()
        func_globals : dict = self._parse()
        self._skip_key()
        func_defaults = self._parse()
        func_defaults = None if func_defaults == None else tuple(func_defaults)
        self._skip_key()
        func_closure = self._parse()
        self._skip_key()
        func_docs = self._parse()
        self._skip_key()
        func_code = self._parse()
        _func = FunctionType(func_code, func_globals, func_name, func_defaults, func_closure)
        _func.__globals__["__builtins__"] = __import__("builtins")
        # _func.__globals__["__math__"] = __import__("math")
        _func.__setattr__("__doc__", func_docs)
        self._get(self.__DTO_TYPES.RBRACE)
        return _func


    def _parse_code(self):
        _code = None
        self._get(self.__DTO_TYPES.STR)
        self._get(self.__DTO_TYPES.COMMA)
        code_dict = self._parse_dict()
        _code = CodeType(
            code_dict["co_argcount"],
            code_dict["co_posonlyargcount"],
            code_dict["co_kwonlyargcount"],
            code_dict["co_nlocals"],
            code_dict["co_stacksize"],
            code_dict["co_flags"],
            code_dict["co_code"],
            tuple(code_dict["co_consts"]),
            tuple(code_dict["co_names"]),
            tuple(code_dict["co_varnames"]),
            code_dict["co_filename"],
            code_dict["co_name"],
            code_dict["co_firstlineno"],
            code_dict["co_lnotab"],
            tuple(code_dict["co_freevars"]),
            tuple(code_dict["co_cellvars"])
        )
        return _code


    def _parse_module(self):
        _module = None
        self._get(self.__DTO_TYPES.STR)
        self._skip_key()
        module_name = self._get(self.__DTO_TYPES.STR)[1]
        self._skip_key()
        if self._check_first()[0] == self.__DTO_TYPES.NULL:
            self._get(self.__DTO_TYPES.NULL)
            _module = __import__(module_name)
        else:
            module_members = self._parse()
            _module = imp.new_module(module_name)
            for field in module_members.items():
                setattr(_module,field[0],field[1])
        self._get(self.__DTO_TYPES.RBRACE)
        return _module


    def _parse_bytes(self):
        _bytes = None
        self._get(self.__DTO_TYPES.STR)
        self._get(self.__DTO_TYPES.COMMA)
        self._skip_key()
        bstring = self._get(self.__DTO_TYPES.STR)
        # _bytes = bytes(bstring[1],'UTF-8')
        _bytes = bytes.fromhex(bstring[1])
        # _bytes = int(bstring[1], 16)
        self._get(self.__DTO_TYPES.RBRACE)
        return _bytes


    def _parse_class(self):
        _class = None
        # skip type field
        self._get(self.__DTO_TYPES.STR)
        # class name
        self._skip_key()
        class_name = self._get(self.__DTO_TYPES.STR)[1]
        # class fields
        self._skip_key()
        class_dict = self._parse()
        class_bases = (object,)
        if "__bases__" in class_dict:
            class_bases = tuple(class_dict["__bases__"])
        _class = type(class_name, class_bases, class_dict)
        self._get(self.__DTO_TYPES.RBRACE) # class rbrace
        return _class


    def _parse_obj(self):
        _obj = None
        # skip type field
        self._get(self.__DTO_TYPES.STR)
        # class name
        self._skip_key()
        class_obj = self._parse()
        # class fields
        self._get(self.__DTO_TYPES.STR)
        self._skip_key()
        obj_dict = self._parse()

        obj_init = class_obj.__init__
        if inspect.isfunction(obj_init):
            if obj_init.__class__.__name__ == "function":
                delattr(class_obj, "__init__")
        _obj = class_obj()
        _obj.__init__ = obj_init
        _obj.__dict__ = obj_dict
        self._get(self.__DTO_TYPES.RBRACE)
        return _obj


    def _parse_nonprimitive(self):
        _obj = None
        self._get(self.__DTO_TYPES.LBRACE)
        if self._check_first()[0] == self.__DTO_TYPES.RBRACE:
            self._get(self.__DTO_TYPES.RBRACE)
            return {}
        elif self._check_first()[1] == 'TYPE':
            self._get(self.__DTO_TYPES.STR)
            self._get(self.__DTO_TYPES.COLON)
            if self._check_first()[1] == self.__DTO_TYPES.FUNC:
                _obj = self._parse_func()
            elif self._check_first()[1] == self.__DTO_TYPES.CODE:
                _obj = self._parse_code()
            elif self._check_first()[1] == self.__DTO_TYPES.CLASS:
                _obj = self._parse_class()
            elif self._check_first()[1] == self.__DTO_TYPES.OBJ:
                _obj = self._parse_obj()
            elif self._check_first()[1] == self.__DTO_TYPES.MODULE:
                _obj = self._parse_module()
            elif self._check_first()[1] == self.__DTO_TYPES.BYTES:
                _obj = self._parse_bytes()
        else:
            _obj = self._parse_dict()
        return _obj


    def _parse(self):
        if self._check_first()[0] == self.__DTO_TYPES.LBRACE:
            return self._parse_nonprimitive()
        elif self._check_first()[0] == self.__DTO_TYPES.LBRACKET:
            return self._parse_list()
        else:
            return self._parse_primitive()
        

    def _parse_first(self):
        obj = self._parse()
        if self._get(self.__DTO_TYPES.EOF)[0] != 'EOF':
            print("OH shit here we go again (the end is not EOF)")
            exit()
        return obj