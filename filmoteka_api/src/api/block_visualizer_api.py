from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

class VisualizerAPI(ABC):
    @abstractmethod
    def __init__(self, visualizer_config: Dict[str, Any]):
        """
        Initialize the visualizer with a configuration.
        """
        self.config = visualizer_config

    @abstractmethod
    def visualize_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Visualize data using the specific visualizer.
        """
        pass