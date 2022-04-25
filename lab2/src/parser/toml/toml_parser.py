import inspect
import imp
import re
from types import FunctionType, CodeType
from src.base_serializator import BaseSerializator

class TomlParser(BaseSerializator):
    __str = ""
    __divided = []


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
        pass