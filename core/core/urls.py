from django.urls import path
from . import views


urlpatterns = [
    path('', views.initial, name='home'),
    path('view', views.view, name='view'),
    path('new-workspace', views.add_new_workspace, name='new-workspace'),
    path('remove-workspace', views.remove_workspace, name='remove-workspace'),
    path('select-workspace', views.select_workspace, name='select-workspace'),
    path('workspaces', views.get_workspaces, name='workspaces')
]