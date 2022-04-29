from pydantic import BaseModel
from typing import Optional


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
	co_code: dict
	co_consts: dict
	co_names: dict
	co_varnames: dict
	co_filename: str
	co_name: str
	co_firstlineno: int
	co_lnotab: dict
	co_freevars: dict
	co_cellvars: dict


class DTO_FUNC(BaseModel):
	DTO_TYPE: str
	name: str
	globals: dict
	defaults: Optional[dict]
	closure: Optional[dict]
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