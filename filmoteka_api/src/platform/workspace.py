import json
from typing import Type, Dict, Any
from api.tmdb_source_api import DataSourceAPI


class Workspace:
    def __init__(self, data_source_plugin: Type[DataSourceAPI], filters: Dict[str, Any], searches: Dict[str, Any]):
        self.data_source_plugin = data_source_plugin
        self.filters = filters
        self.searches = searches

    def save_state(self, file_path: str):
        state = {
            'data_source_plugin': self.data_source_plugin.__name__,
            'filters': self.filters,
            'searches': self.searches
        }
        with open(file_path, 'w') as f:
            json.dump(state, f)

    @classmethod
    def load_state(cls, file_path: str) -> 'Workspace':
        with open(file_path, 'r') as f:
            state = json.load(f)
        # Assuming all plugins are imported and available in globals()
        data_source_plugin = globals()[state['data_source_plugin']]
        return cls(data_source_plugin, state['filters'], state['searches'])
