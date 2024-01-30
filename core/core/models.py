class NodeAttribute:
    id = 0

    def __init__(self, name: str, value: object):
        super().__init__()
        self.name = name
        self.value = value
        self.id = NodeAttribute.id
        NodeAttribute.id += 1

    def __str__(self):
        return self.name + ": " + self.value.__str__()


class Node:
    id = 0

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.attributes = []
        self.id = Node.id
        Node.id += 1

    def add_attribute(self, name: str, value: object):
        self.attributes.append(NodeAttribute(name, value))

    def __str__(self):
        string = self.name + "\n"
        for attribute in self.attributes:
            string += "\t" + attribute.__str__() + "\n"
        return string


class Edge:
    id = 0

    def __init__(self, directed: bool, fromNode: Node, toNode: Node, type: str):
        super().__init__()
        self.directed = directed
        self.fromNode = fromNode
        self.toNode = toNode
        self.type = type
        self.id = Edge.id
        Edge.id += 1

    def __str__(self):
        return self.fromNode.name + "->" + self.toNode.name


class Graph:
    # id = 0

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        # self.id = Graph.id
        # Graph.id += 1

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def __str__(self):
        string = ""
        for node in self.nodes:
            string += node.__str__() + "\n"
        for edge in self.edges:
            string += edge.__str__() + "\n"
        return string


class Workspace:
    id = 1

    def __init__(self, data_source_id: str,
                 search_param: str = "", filter_params: list[str] = None):

        self.id = Workspace.id
        Workspace.id += 1

        self.data_source_id = data_source_id
        self.search_param = search_param
        self.filter_params = filter_params
        self.name = data_source_id + ' #' + str(self.id)

    def update(self, search_param: str = "", filter_params: list[str] = None):
        self.search_param = search_param
        self.filter_params = filter_params

    def __str__(self):
        return self.name

