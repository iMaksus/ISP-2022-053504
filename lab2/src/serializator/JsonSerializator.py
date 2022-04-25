from src.serializer.json import JsonSerializer
from src.parser.json import JsonParser

class JsonSerializator(JsonSerializer, JsonParser):
    Serializer = JsonSerializer()
    def loads(self):
        self.loads