from abc import ABC, abstractmethod

class VisualizationService(ABC):

    @abstractmethod
    def visualize_graph(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def id(self):
        pass