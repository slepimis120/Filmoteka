from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


class DataSourceAPI(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def fetch_data(self, movie_id: str, tmdb_key: str):
        pass