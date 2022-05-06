
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('project/<str:pk>/', views.project,name="project"),
    path('create_project', views.create_project,name="create_project"),
]