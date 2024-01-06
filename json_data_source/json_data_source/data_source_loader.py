from core.core.models import Node, NodeAttribute, Graph, Edge
from core.core.services.data_source_service import DataSourceService
import json


class JsonDataSourceLoader(DataSourceService):

    def id(self):
        pass

    def name(self):
        return "json"

    def __init__(self):
        pass

    def load_node_attributes(self, data):
        node_attributes = []
        for el in data:
            if el != "predators":
                node_attribute = NodeAttribute(el, data[el])
                node_attributes.append(node_attribute)
        return node_attributes

    def load_nodes(self, data, graph):
        for obj in data:
            node = Node(obj["name"])
            node.attributes = self.load_node_attributes(obj["characteristics"])
            graph.add_node(node)

    def find_node(self, graph, name):
        nodes = []
        for node in graph.nodes:
            if name in node.name:
                nodes.append(node)
        return nodes

    def construct_edge(self, name, predator, graph):
        from_node = self.find_node(graph, predator)
        to_node = self.find_node(graph, name)[0]
        if from_node != [] and to_node is not None:
            for node in from_node:
                edge = Edge(True, node, to_node, "predator")
                graph.add_edge(edge)

    def load_edges(self, data, graph):
        for obj in data:
            try:
                predators = [p.strip() for p in obj["characteristics"]["predators"].split(",")]
                for predator in predators:
                    if " and " in predator:
                        predators = predator.split(" and ")
                        for p in predators:
                            self.construct_edge(obj["name"], p, graph)
                    else:
                        self.construct_edge(obj["name"], predator, graph)
            except KeyError:
                pass

    def load_graph(self, data):
        graph = Graph()
        self.load_nodes(data, graph)
        self.load_edges(data, graph)
        return graph

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return self.load_graph(data)
