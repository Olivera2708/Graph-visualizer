from django.shortcuts import render, redirect
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
    return redirect('home')


def start_source_plugins(source_plugins, file_name):
    for plugin in source_plugins:
        if plugin.name() == file_name.split(".")[1]:
            return plugin.load_data(get_path(file_name))

def get_path(file_name):
    file_path = "core/core/static/" + file_name
    absolute_file_path = os.path.abspath(file_path)
    return absolute_file_path
