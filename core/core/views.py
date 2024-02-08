import json
import os
import re
import traceback
from datetime import datetime, date
from copy import deepcopy

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
    return JsonResponse({'plugins': ids})

def get_visualization_options(request):
    config = apps.get_app_config('core')
    ids = [plugin.id() for plugin in config.visualizer_plugins]
    return JsonResponse({'options': ids})


def add_new_workspace(request):
    data_source_id = request.POST.get("data_source_id")

    config = apps.get_app_config('core')
    data_plugins = config.data_source_plugins

    search = request.POST.get('search_param')
    filter_params_request = request.POST.get('filter_params')
    filter_params = None
    if filter_params_request:
        filter_params = json.loads(filter_params_request)
    root_node = request.POST.get('root_node')

    config.update_workspace(search, filter_params, root_node)

    graph = start_source_plugin(data_plugins, data_source_id)

    config.add_workspace(data_source_id, graph)
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

    config.select_workspace(request.GET.get('name'))
    response = {'search_param': config.selected_workspace.search_param,
                'filter_params': config.selected_workspace.filter_params,
                'root_node': config.selected_workspace.root_node}
    return JsonResponse(response)


def get_current_workspace(request):
    config = apps.get_app_config('core')
    if config.selected_workspace:
        response = {'search_param': config.selected_workspace.search_param,
                    'filter_params': config.selected_workspace.filter_params,
                    'root_node': config.selected_workspace.root_node}
    else:
        response = {}
    return JsonResponse(response)


def view(request):
    search_query = request.POST.get('search').strip()
    visualizer_id = request.POST.get("visualizer")
    filter_params_request = request.POST.get('filter_params')
    filter_params = None
    if filter_params_request:
        filter_params = json.loads(request.POST.get('filter_params'))

    config = apps.get_app_config('core')
    visualizer_plugins = config.visualizer_plugins

    if not config.selected_workspace:
        return JsonResponse({"template": ""})

    try:
        graph = deepcopy(config.selected_workspace.graph)

        search_graph(graph, search_query)
        messages = filter_graph(graph, filter_params)
        for message in messages:
            print(message)
        print(len(graph.nodes))
        html = run_visualisation_plugins(visualizer_plugins, visualizer_id, graph)
        tree_html = load_tree(graph)
        bird_html = load_bird(graph)
        return JsonResponse({"template": html, "tree": tree_html, "bird": bird_html})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"template": ""})


def run_visualisation_plugins(visualisation_plugins, visualizer_id, graph):
    global template
    template = None
    for plugin in visualisation_plugins:
        if plugin.id() == visualizer_id:
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
    if search_query == "":
        return
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
        if found:
            continue
        removed_nodes.append(node)

    if len(removed_nodes) > 0:
        remove_nodes(graph, removed_nodes)


def remove_nodes(graph, nodes):
    removed_edges = []

    for edge in graph.edges:
        if edge.fromNode in nodes or edge.toNode in nodes:
            removed_edges.append(edge)

    for edge in removed_edges:
        graph.remove_edge(edge)

    for node in nodes:
        graph.remove_node(node)


def filter_graph(graph, filter_params):
    messages = []
    removed_nodes = []
    no_attribute_nodes = []
    for filter_param in filter_params:
        name_expression, operator, value_expression = extract_tokens(filter_param)

        found_attribute_in_graph = False
        for node in graph.nodes:
            found_attribute_in_node = False
            for attribute in node.attributes:
                if attribute.name.lower().strip() != name_expression:
                    continue
                print(type(attribute.value).__name__)
                found_attribute_in_node = True
                found_attribute_in_graph = True
                parsed_value, adapted_value, message = parse_by_type(value_expression, attribute.value)
                if message is not None:
                    messages.append(message)
                    continue
                if not compare(adapted_value, operator, parsed_value) and node not in removed_nodes:
                    removed_nodes.append(node)
                break
            if not found_attribute_in_node:
                no_attribute_nodes.append(node)
        if not found_attribute_in_graph:
            messages.append(f"No such attribute as {name_expression}")
        else:
            for node in no_attribute_nodes:
                if node not in removed_nodes:
                    removed_nodes.append(node)
        no_attribute_nodes.clear()

    if len(removed_nodes) > 0:
        remove_nodes(graph, removed_nodes)
    return messages


def extract_tokens(filter_param):
    expression_regex = r'^\s*([\w\d\s,.\-()]+)\s*(==|>|>=|<|<=|!=)\s*([\w\d\s,.\-()]+)\s*$'
    match = re.match(expression_regex, filter_param)
    name_expression = match.group(1).strip()
    operator = match.group(2).strip()
    value_expression = match.group(3).strip()
    return name_expression.lower().strip(), operator.strip(), value_expression.lower().strip()


def parse_by_type(value_expression, value_of_type):
    parsed_value = None
    adapted_value = value_of_type
    message = None
    try:
        if isinstance(value_of_type, date):
            parsed_value = datetime.strptime(value_expression, "%Y-%m-%d").date()
        elif isinstance(value_of_type, int):
            parsed_value = int(value_expression)
        elif isinstance(value_of_type, float):
            parsed_value = float(value_expression)
        elif isinstance(value_of_type, str):
            parsed_value = value_expression
            adapted_value = value_of_type.lower().strip()
    except Exception as e:
        message = f"{value_expression} cannot be interpreted as {type(value_of_type).__name__}"
    finally:
        return parsed_value, adapted_value, message


def compare(attribute_value, operator, value_expression):
    if operator == "==":
        return attribute_value == value_expression
    elif operator == ">":
        return attribute_value > value_expression
    elif operator == ">=":
        return attribute_value >= value_expression
    elif operator == "<":
        return attribute_value < value_expression
    elif operator == "<=":
        return attribute_value <= value_expression
    elif operator == "!=":
        return attribute_value != value_expression
    return False
