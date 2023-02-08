# from django.urls import path
# from interpreter import views

# urlpatterns = [
#     path('', views.index)
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('interpreter.urls')),
]