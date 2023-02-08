from django.urls import path
from interpreter_app import views

urlpatterns = [
    path('', views.index)
]