from django.shortcuts import render, redirect
from django.apps.registry import apps
import os
from django.contrib import messages
import traceback
from .models import *

node1 = Node("NAMEEEEEEEEEEEEEEEEEE")
node2 = Node("name2")
node3 = Node("name3")

node1.add_attribute("naziv1", "vrednost1")
node1.add_attribute("naziv2", "vrednost2")
node2.add_attribute("naziv3", "vrednost3")
node3.add_attribute("naziv4", "vrednost4")

edge1 = Edge(True, node1, node2, "type")
edge2 = Edge(False, node1, node3, "type")


def initial(request):
    return render(request, 'index.html')


def view(request):
    config = apps.get_app_config('core')
    config.load_plugins()
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins
    try:
        html = run_visualisation_plugins(visualizer_plugins, request)
        nodes, edges = [node1, node2, node3], [edge1, edge2]
        return render(request, "index.html", {"template": html, "nodes": nodes, "edges": edges})
    except FileNotFoundError:
        messages.error(request, "File doesn't exist!")
        return render(request, "index.html")
    except Exception as e:
        traceback.print_exc()
        return redirect('home')

def run_visualisation_plugins(visualisation_plugins, request):
    for plugin in visualisation_plugins:
        # if plugin.name() == request.POST['visualizer']:
        global template
        template = plugin.load()
    html = template.render(nodes=[node1, node2, node3], edges=[edge1, edge2])
    return html
