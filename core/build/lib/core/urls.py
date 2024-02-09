from django.urls import path
from . import views


urlpatterns = [
    path('', views.initial, name='home'),
    path('view', views.view, name='view'),
    path('source-plugins', views.get_data_source_plugins, name='source-plugins'),
    path('visualization-options', views.get_visualization_options, name='visualization-options'),
    path('new-workspace', views.add_new_workspace, name='new-workspace'),
    path('remove-workspace', views.remove_workspace, name='remove-workspace'),
    path('select-workspace', views.select_workspace, name='select-workspace'),
    path('get-workspace', views.get_current_workspace, name='get-workspace'),
    path('workspaces', views.get_workspaces, name='workspaces'),
    path('check-filter', views.check_filter, name='check-filter')
]