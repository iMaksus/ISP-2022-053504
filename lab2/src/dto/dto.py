from pydantic import BaseModel
from typing import Optional

class DTO_code_func(BaseModel):
	TYPE: str
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

class DTO_func(BaseModel):
	TYPE: str
	name: str
	globals: dict
	defaults: Optional[tuple]
	closure: Optional[tuple]
	code: dict

class DTO_class(BaseModel):
	TYPE: str
	name: str
	fields: dict

class DTO_obj(BaseModel):
	TYPE: str
	obj_class: dict
	fields: dict