from django.contrib import admin
from django.urls import path
from django_example_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("chat", views.chat, name="chat"),
    path("stream", views.stream, name="stream"),
    path("reset", views.reset_chat, name="reset"),
]
