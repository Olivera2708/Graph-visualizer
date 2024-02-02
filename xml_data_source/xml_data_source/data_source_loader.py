import xml.etree.ElementTree as ET
from datetime import datetime

from core.core.models import Node, Graph, Edge
from core.core.services.data_source_service import DataSourceService


class XMLDataSourceLoader(DataSourceService):
    
    def id(self):
        return "people xml"

    def name(self):
        return "xml"

    def file_name(self):
        return "data.xml"

    def __init__(self):
        pass

    def load_data(self, file_path: str):
        graph = Graph()
        data = ET.parse(file_path)
        root = data.getroot()
        self.load_nodes(graph, root)
        self.load_edges(graph)
        return graph


    def load_nodes(self, graph: Graph, root: ET.Element):
        for row in root:
            name = row.find('name')
            node = Node(name.find('first').text.replace('\n', '').strip()
                        + ' ' + name.find('last').text.replace('\n', '').strip())
            self._load_node_attributes(node, row)
            graph.add_node(node)

    
    def _load_node_attributes(self, node: Node, element: ET.Element):
        for child in element:
            if not child.text: continue
            text: str = child.text.strip().replace('\n', '').strip()
            value: object = text
            if text:
                if child.tag in ['birthday', 'memberSince']:
                    value = datetime.strptime(text, '%Y-%m-%d').date()
                node.add_attribute(child.tag, value)
            else:
                self._load_node_attributes(node, child)


    def load_edges(self, graph: Graph):
        n = len(graph.nodes)
        for i in range(n-1):
            from_node = graph.nodes[i]
            for j in range(i+1, n):
                to_node = graph.nodes[j]
                if self._have_same_likes(from_node, to_node):
                    self._make_edge(graph, from_node, to_node)



    def _have_same_likes(self, from_node: Node, to_node: Node):
        for from_attribute in from_node.attributes:
            for to_attribute in to_node.attributes:
                if (from_attribute.name == to_attribute.name == 'likes'
                and from_attribute.value == to_attribute.value):
                    return True
        return False


    def _make_edge(self, graph: Graph, from_node: Node, to_node: Node):
        edge = Edge(False, from_node, to_node, "mutual interest")
        graph.add_edge(edge)
