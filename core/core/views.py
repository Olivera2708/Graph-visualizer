from django.shortcuts import render, redirect
from django.apps.registry import apps



def initial(request):
    return render(request, 'index.html')

def view(request):
    config = apps.get_app_config('core')
    data_source_plugins = config.data_source_plugins
    visualizer_plugins = config.visualizer_plugins
    return redirect('home')
