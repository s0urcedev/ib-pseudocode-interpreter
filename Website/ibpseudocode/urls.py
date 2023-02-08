from django.urls import path
from interpreter import views

urlpatterns = [
    path('', views.index)
]
