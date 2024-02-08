from abc import ABC, abstractmethod

class VisualizationService(ABC):

    @abstractmethod
    def load(self) -> str:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def id(self) -> str:
        pass