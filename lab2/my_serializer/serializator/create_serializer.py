from .json_serializator import JsonSerializator
from .toml_serializator import TomlSerializator
from .yaml_serializator import YamlSerializator
from ..base_serializator import BaseSerializator

FORMATS = {
    "json": JsonSerializator,
    "toml": TomlSerializator,
    "yaml": YamlSerializator
}

def create_serializer(name : str) -> BaseSerializator:
    if name in FORMATS:
        return FORMATS[name]()
    else:
        return None