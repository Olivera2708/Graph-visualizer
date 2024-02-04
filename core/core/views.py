import json
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


def get_data_source_plugins(request):
    config = apps.get_app_config('core')
    ids = [plugin.id() for plugin in config.data_source_plugins]
    print(ids)
    return JsonResponse({'plugins': ids})


def add_new_workspace(request):
    data_source_id = request.POST.get("data_source_id")

    config = apps.get_app_config('core')

    search = request.POST.get('search_param')
    filter_params_request = request.POST.get('filter_params')
    filter_params = None
    if filter_params_request:
        filter_params = json.loads(filter_params_request)
    root_node = request.POST.get('root_node')

    config.update_workspace(search, filter_params, root_node)

    config.add_workspace(data_source_id)

    print([ws.name for ws in config.workspaces])
    return HttpResponse()


def remove_workspace(request):
    config = apps.get_app_config('core')
    config.remove_workspace(request.GET.get('name'))
    return HttpResponse()


def select_workspace(request):
    config = apps.get_app_config('core')

    search = request.GET.get('search_param')
    filter_params_request = request.GET.get('filter_params')
    filter_params = None
    if filter_params_request:
        filter_params = json.loads(filter_params_request)
    root_node = request.GET.get('root_node')

    config.update_workspace(search, filter_params, root_node)

    print(config.selected_workspace.search_param)
    config.select_workspace(request.GET.get('name'))
    response = {'search_param': config.selected_workspace.search_param,
                'filter_params': config.selected_workspace.filter_params,
                'root_node': config.selected_workspace.root_node}
    print(config.selected_workspace.search_param)
    return JsonResponse(response)


def get_current_workspace(request):
    config = apps.get_app_config('core')
    if config.selected_workspace:
        response = {'search_param': config.selected_workspace.search_param,
                    'filter_params': config.selected_workspace.filter_params,
                    'root_node': config.selected_workspace.root_node}
        print(config.selected_workspace.root_node)
    else:
        response = {}
    return JsonResponse(response)


def view(request):
    search_query = request.POST.get('search').strip()
    visualizer = request.POST.get("visualizer")
    filter_params_request = request.POST.get('filter_params')
    filter_params = None
    if filter_params_request:
        filter_params = json.loads(request.POST.get('filter_params'))

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
        search_graph(graph, search_query)

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


def start_source_plugin(source_plugins, source_id):
    for plugin in source_plugins:
        if plugin.id() == source_id:
            return plugin.load_data(get_path(plugin.file_name()))


def load_tree(graph):
    template = get_template("tree.html")
    if graph.edges:
        relation_type = graph.edges[0].type
    else:
        relation_type = None

    return template.render(nodes=graph.nodes, edges=graph.edges, relation=relation_type)


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


def search_graph(graph, search_query):
    if search_query == "": return
    removed_nodes = []
    for node in graph.nodes:
        if search_query.upper() in node.name.upper():
            continue
        found = False
        for attribute in node.attributes:
            if (
                    search_query.upper() in attribute.name.upper() or
                    search_query.upper() in str(attribute.value).upper()
            ):
                found = True
                break
        if found: continue
        removed_nodes.append(node)

    if len(removed_nodes) == 0:
        return

    removed_edges = []

    for edge in graph.edges:
        if edge.fromNode in removed_nodes or edge.toNode in removed_nodes:
            removed_edges.append(edge)

    for edge in removed_edges:
        graph.remove_edge(edge)

    for node in removed_nodes:
        graph.remove_node(node)
