from ..base_serializator import BaseSerializator
from ..serializer import YamlSerializer
from ..parser import YamlParser

class YamlSerializator(BaseSerializator):
    __serializer = YamlSerializer()
    __parser = YamlParser()

    
    def dump(self, obj : any, file_path : str):
        self.__serializer.dump(obj, file_path)

        
    def dumps(self, obj : any) -> str:
        return self.__serializer.dumps(obj)


    def load(self, file_path : str) -> any:
        return self.__parser.load(file_path)


    def loads(self, _str : str) -> any:
        return self.__parser.loads(_str)