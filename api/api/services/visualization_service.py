from abc import ABC, abstractmethod

class VisualizationService(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def id(self):
        pass