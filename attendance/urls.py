"""URLs"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app_main import cam, views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # home end points
    path(
        "home/employees", views.AllEmployeesView.as_view(), name="all_employees"
    ),
    path("home/vacation", views.VacationView.as_view(), name="vacation"),
    path("home/working", views.WorkingView.as_view(), name="working"),
    path("home/sick", views.SickView.as_view(), name="sick"),
    path("home/other", views.OtherView.as_view(), name="other"),
    # others
    path("cam/<int:speed>", views.CamView.as_view(), name="cam"),
    path("cam/video_stream/<int:speed>", cam.video_stream, name="video_stream"),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
