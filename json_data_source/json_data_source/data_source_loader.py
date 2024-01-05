from core.core.services.data_source_service import DataSourceService
import json


class JsonDataSourceLoader(DataSourceService):

    def id(self):
        pass
    def name(self):
        return "json"

    def __init__(self):
        pass

    def load_data(self, file_path):
        file = open(file_path, 'r')
        data = json.load(file)
        print(data)
        # load to graph
        file.close()
