from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


class DataSourceAPI(ABC):
    @abstractmethod
    def __init__(self, data_source_config: Dict[str, Any]):
        """
        Initialize the data source with a configuration.
        """
        self.config = data_source_config

    @abstractmethod
    def connect(self):
        """
        Establish a connection to the data source.
        """
        pass

    @abstractmethod
    def fetch_data(self, query: str) -> Union[List[Dict[str, Any]], None]:
        """
        Fetch data from the data source based on the provided query.
        """
        pass

    @abstractmethod
    def close_connection(self):
        """
        Close the connection to the data source.
        """
