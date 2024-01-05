import os
from jinja2 import FileSystemLoader, Environment
from core.core.services.visualization_service import VisualizationService

class SimpleVisualisation(VisualizationService):

    def name(self):
        return "SimpleVisualisation"

    def id(self):
        pass

    def visualize_graph(request):
        pass

    def load(self):
        p = os.path.dirname(__file__)
        path = os.path.join(p, "templates")
        env = Environment(loader=FileSystemLoader(searchpath=path))
        template = env.get_template('simpleVisualizer.html')
        return template
