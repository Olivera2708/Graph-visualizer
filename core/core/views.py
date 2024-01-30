import os
import traceback

from django.apps import apps
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from jinja2 import FileSystemLoader, Environment


def initial(request):
    config = apps.get_app_config('core')
    config.load_plugins()
    return render(request, 'index.html')


def get_workspaces(request):
    config = apps.get_app_config('core')
    response = {'tabs': config.get_tabs()}
    return JsonResponse(response)


def add_new_workspace(request):
    data_source = request.POST.get("data_source")
    if data_source is None:
        data_source_id = "animals json"
    else:
        data_source_id = "people xml"
    config = apps.get_app_config('core')
    config.add_workspace(data_source_id)

    print([ws.name for ws in config.workspaces])
    return HttpResponse()


def remove_workspace(request):
    config = apps.get_app_config('core')
    config.remove_workspace(request.GET.get('name'))
    return HttpResponse()

def select_workspace(request):
    config = apps.get_app_config('core')
    config.select_workspace(request.GET.get('name'))
    return HttpResponse()



def view(request):
    search = request.POST.get('search')
    visualizer = request.POST.get("visualizer")

    if visualizer is None:
        visualizer_name = "SimpleVisualizer"
    else:
        visualizer_name = "BlockVisualizer"

    config = apps.get_app_config('core')
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins

    if not config.selected_workspace:
        return JsonResponse({"template": ""})

    try:
        graph = start_source_plugin(data_source_plugins, config.selected_workspace.data_source_id)
        html = run_visualisation_plugins(visualizer_plugins, visualizer_name, graph)
        tree_html = load_tree(graph)

        #todo save search and filter params
        config.update_workspace(config.selected_workspace.data_source_id)
        print(config.selected_workspace)

        return JsonResponse({"template": html, "tree": tree_html})
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


def start_source_plugin(source_plugins, source_id):
    for plugin in source_plugins:
        if plugin.id() == source_id:
            return plugin.load_data(get_path(plugin.file_name()))



def load_tree(graph):
    template = get_template("tree.html")
    return template.render(nodes=graph.nodes, edges=graph.edges, relation=graph.edges[0].type)

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
