from pydantic import BaseModel
from typing import Optional

class DTO_LIST(BaseModel):
    DTO_TYPE: str
    TYPE_INT: list
    TYPE_STR: list
    TYPE_BOOL: list
    TYPE_NONE: list


class DTO_BYTES(BaseModel):
	DTO_TYPE: str
	field: str


class DTO_CODE(BaseModel):
	DTO_TYPE: str
	co_argcount: int
	co_posonlyargcount: int
	co_kwonlyargcount: int
	co_nlocals: int
	co_stacksize: int
	co_flags: int
	co_code: bytes
	co_consts: tuple
	co_names: tuple
	co_varnames: tuple
	co_filename: str
	co_name: str
	co_firstlineno: int
	co_lnotab: bytes
	co_freevars: tuple
	co_cellvars: tuple


class DTO_FUNC(BaseModel):
	DTO_TYPE: str
	name: str
	globals: dict
	defaults: Optional[tuple]
	closure: Optional[tuple]
	docs: Optional[str]
	code: dict


class DTO_CLASS(BaseModel):
	DTO_TYPE: str
	name: str
	fields: dict


class DTO_OBJ(BaseModel):
	DTO_TYPE: str
	obj_class: dict
	fields: dict


class DTO_MODULE(BaseModel):
	DTO_TYPE: str
	name: str
	attrs: Optional[dict]