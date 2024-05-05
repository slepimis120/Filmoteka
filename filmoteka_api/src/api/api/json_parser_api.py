from abc import ABC, abstractmethod


class JSONParserAPI(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def parse(self, file):
        pass