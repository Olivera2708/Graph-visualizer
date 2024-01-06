from django.shortcuts import render, redirect
from django.apps import apps
import os


def initial(request):
    return render(request, 'index.html')


def view(request):
    search = request.POST.get('search')
    data_source = request.POST.get("data_source")
    visualizer = request.POST.get("visualizer")

    print("\n\nData Source:", data_source)
    print("Visualizer:", visualizer)
    print("\n\n")

    if data_source is None:
        file_name = "data.json"
    else:
        file_name = "data.xml"

    if visualizer is None:
        visualizer_name = "simple"
    else:
        visualizer_name = "block"

    config = apps.get_app_config('core')
    config.load_plugins()
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins

    graph = start_source_plugins(data_source_plugins, file_name)

    return redirect('home')


def start_source_plugins(source_plugins, file_name):
    for plugin in source_plugins:
        if plugin.name() == file_name.split(".")[1]:
            return plugin.load_data(get_path(file_name))


def get_path(file_name):
    file_path = "core/core/static/" + file_name
    absolute_file_path = os.path.abspath(file_path)
    return absolute_file_path
