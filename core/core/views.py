from django.shortcuts import render, redirect
from django.contrib import messages
import traceback
from django.apps import apps
import os

def initial(request):
    return render(request, 'index.html')


def view(request):
    config = apps.get_app_config('core')
    config.load_plugins()
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins
    graph = start_source_plugins(data_source_plugins, "data.json")
    try:
        html = run_visualisation_plugins(visualizer_plugins, request, graph)
        nodes, edges = graph.nodes, graph.edges
        return render(request, "index.html", {"template": html, "nodes": nodes, "edges": edges})
    except FileNotFoundError:
        messages.error(request, "File doesn't exist!")
        return render(request, "index.html")
    except Exception as e:
        traceback.print_exc()
        return redirect('home')

def run_visualisation_plugins(visualisation_plugins, request, graph):
    for plugin in visualisation_plugins:
        # if plugin.name() == request.POST['visualizer']:
        global template
        template = plugin.load()
    html = template.render(nodes=graph.nodes, edges=graph.edges)
    return html

def start_source_plugins(source_plugins, file_name):
    for plugin in source_plugins:
        if plugin.name() == file_name.split(".")[1]:
            return plugin.load_data(get_path(file_name))

def get_path(file_name):
    file_path = "core/core/static/" + file_name
    absolute_file_path = os.path.abspath(file_path)
    return absolute_file_path
