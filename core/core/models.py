from api.models import Graph


class Workspace:
    id = 1

    def __init__(self, data_source_id: str, graph: Graph = None, search_param: str = "",
                 filter_params: list[str] = None, root_node: str = ""):

        self.id = Workspace.id
        Workspace.id += 1

        self.data_source_id = data_source_id
        self.search_param = search_param
        self.filter_params = filter_params
        self.root_node = root_node
        self.graph = graph
        self.name = data_source_id + ' #' + str(self.id)

    def update(self, search_param: str = "", filter_params: list[str] = None, root_node: str = ''):
        self.search_param = search_param
        self.filter_params = filter_params
        self.root_node = root_node

    def __str__(self):
        return self.name
