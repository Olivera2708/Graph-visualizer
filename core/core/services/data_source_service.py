from abc import ABC, abstractmethod


class DataSourceService(ABC):

    @abstractmethod
    def load_data(self, file_path):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def id(self):
        pass