from django.urls import path
from interpreter.views import index


urlpatterns = [
    path('', index),
]