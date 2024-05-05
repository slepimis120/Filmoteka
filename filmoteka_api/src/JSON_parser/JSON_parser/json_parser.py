import json

from api.json_parser_api import JSONParserAPI
from api.model import Graph, Node


class JSONParser(JSONParserAPI):
    def name(self):
        return "JSON parser"

    def identifier(self):
        return "json_parser"

    def parse(self, file):
        pass