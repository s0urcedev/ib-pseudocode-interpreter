from django.urls import path
from interpreter_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('syntax', views.syntax)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)