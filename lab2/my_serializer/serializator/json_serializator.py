from ..base_serializator import BaseSerializator
from ..serializer import JsonSerializer
from ..parser import JsonParser

class JsonSerializator(BaseSerializator):
    __serializer = JsonSerializer()
    __parser = JsonParser()

    
    def dump(self, obj : any, file_path : str):
        self.__serializer.dump(obj, file_path)

        
    def dumps(self, obj : any) -> str:
        return self.__serializer.dumps(obj)


    def load(self, file_path : str) -> any:
        return self.__parser.load(file_path)


    def loads(self, _str : str) -> any:
        return self.__parser.loads(_str)