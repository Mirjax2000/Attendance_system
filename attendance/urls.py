from django.contrib import admin
from django.urls import path

from app_main import views

handler404 = "app_main.views.custom_404"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("cam/", views.cam, name="cam"),
    path("video_stream/", views.video_stream, name="video_stream"),
]
