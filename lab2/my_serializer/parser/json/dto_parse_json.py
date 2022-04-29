from pydantic import BaseModel


class DTO_REGEX(BaseModel):
    LBRACE = r"{"
    RBRACE = r"}"
    LBRACKET = "\\["
    RBRACKET = "\\]"
    COLON = r":"
    COMMA = r","
    NULL = r'null'
    STR = r'"[^"]*"'
    NUMBER = r'([0-9]*[.])?[0-9]+'
    BOOL = r'^(?:tru|fals)e'
    EOF = "EOF"

class DTO_TYPES(BaseModel):
    FUNC = "func"
    CODE = "code"
    CLASS = "class"
    OBJ = "obj"
    MODULE = "module"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    COMMA = "COMMA"
    NULL = "NULL"
    STR = "STR"
    BYTES = "bytes"
    NUMBER = "NUMBER"
    BOOL = "BOOL"
    EOF = "EOF"