from pydantic import BaseModel

class DTO_TYPES(BaseModel):
    STR = "TYPE_STR"
    NUMBER = "TYPE_NUMBER"
    BOOL = "TYPE_BOOL"
    NONE = "TYPE_STR"
    BYTES = "bytes"
    CLASS = "class"
    OBJ = "obj"
    FUNC = "func"
    MODULE = "module"
    CODE = "code"
    LIST = "list"


class DTO_FIELDS_BYTES(BaseModel):
	field = "field"


class DTO_FIELDS_CODE(BaseModel):
	co_argcount = "co_argcount"
	co_posonlyargcount = "co_posonlyargcount"
	co_kwonlyargcount = "co_kwonlyargcount"
	co_nlocals = "co_nlocals"
	co_stacksize = "co_stacksize"
	co_flags = "co_flags"
	co_code = "co_code"
	co_consts = "co_consts"
	co_names = "co_names"
	co_varnames = "co_varnames"
	co_filename = "co_filename"
	co_name = "co_name"
	co_firstlineno = "co_firstlineno"
	co_lnotab = "co_lnotab"
	co_freevars = "co_freevars"
	co_cellvars = "co_cellvars"


class DTO_FIELDS_FUNC(BaseModel):
	name = "name"
	globals = "globals"
	defaults = "defaults"
	closure = "closure"
	docs = "docs"
	code = "code"


class DTO_FIELDS_CLASS(BaseModel):
	name = "name"
	fields = "fields"


class DTO_FIELDS_OBJ(BaseModel):
	obj_class = "obj_class"
	fields = "fields"


class DTO_FIELDS_MODULE(BaseModel):
	name = "name"
	attrs = "attrs"