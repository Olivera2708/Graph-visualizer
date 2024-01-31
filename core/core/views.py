from django.http import JsonResponse
from django.shortcuts import render
from jinja2 import FileSystemLoader, Environment
import traceback
from django.apps import apps
import os

def initial(request):
    return render(request, 'index.html')

def view(request):
    search = request.POST.get('search')
    data_source = request.POST.get("data_source")
    visualizer = request.POST.get("visualizer")

    if data_source is None:
        file_name = "data.json"
    else:
        file_name = "data.xml"

    if visualizer is None:
        visualizer_name = "SimpleVisualizer"
    else:
        visualizer_name = "BlockVisualizer"

    config = apps.get_app_config('core')
    config.load_plugins()
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins

    try:
        graph = start_source_plugins(data_source_plugins, file_name)
        html = run_visualisation_plugins(visualizer_plugins, visualizer_name, graph)
        tree_html = load_tree(graph)
        bird_html = load_bird(graph)
        return JsonResponse({"template": html, "tree": tree_html, "bird": bird_html})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"template": ""})

def run_visualisation_plugins(visualisation_plugins, visualizer_name, graph):
    global template
    template = None
    for plugin in visualisation_plugins:
        if plugin.name() == visualizer_name:
            template = plugin.load()
    html = template.render(nodes=graph.nodes, edges=graph.edges)
    return html

def start_source_plugins(source_plugins, file_name):
    for plugin in source_plugins:
        if plugin.name() == file_name.split(".")[1]:
            return plugin.load_data(get_path(file_name))

def load_tree(graph):
    template = get_template("tree.html")
    return template.render(nodes=graph.nodes, edges=graph.edges, relation=graph.edges[0].type)

def load_bird(graph):
    template = get_template("bird.html")
    return template.render()

def get_template(view):
    p = os.path.dirname(__file__)
    path = os.path.join(p, "templates")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template(view)
    return template

def get_path(file_name):
    file_path = "core/core/static/" + file_name
    absolute_file_path = os.path.abspath(file_path)
    return absolute_file_path
