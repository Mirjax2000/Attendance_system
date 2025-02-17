from django.contrib import admin
from django.urls import path

from app_main import views
from django.conf.urls.static import static
from django.conf import settings

handler404 = "app_main.views.custom_404"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("cam/<int:speed>", views.cam, name="cam"),
    path("cam/video_stream/<int:speed>", cam.video_stream, name="video_stream"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
