from abc import ABC, abstractmethod


class BaseSerializator(ABC):
    @abstractmethod
    def dump(self, obj: any, file_path: str):
        """ abstract method """
    @abstractmethod
    def dumps(self, obj: any) -> str:
        """ abstract method """
    @abstractmethod
    def load(self, file_path: str) -> any:
        """ abstract method """
    @abstractmethod
    def loads(self, _str: str) -> any:
        """ abstract method """