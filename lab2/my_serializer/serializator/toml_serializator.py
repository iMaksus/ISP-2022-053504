from ..base_serializator import BaseSerializator
from ..serializer import TomlSerializer
from ..parser import TomlParser

class TomlSerializator(BaseSerializator):
    __serializer = TomlSerializer()
    __parser = TomlParser()

    
    def dump(self, obj : any, file_path : str):
        self.__serializer.dump(obj, file_path)

        
    def dumps(self, obj : any) -> str:
        return self.__serializer.dumps(obj)


    def load(self, file_path : str) -> any:
        return self.__parser.load(file_path)


    def loads(self, _str : str) -> any:
        return self.__parser.loads(_str)