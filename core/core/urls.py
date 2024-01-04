from django.urls import path
from . import views


urlpatterns = [
    path('', views.initial, name='home'),
    path('view', views.view, name='view')
]