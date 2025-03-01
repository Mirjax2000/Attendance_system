"""URLs"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from app_dashboard.views import (
    AttendanceView,
    ChartsView,
    DashboardView,
    EmailView,
    EmployeesView,
    MainPanelView,
    OtherView,
    SickView,
    VacationView,
    WorkingView,
)
from app_main.cam import cam_stream
from app_main.views import MainPageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("camstream/<int:speed>", cam_stream, name="camstream"),
]

app_main_urls: list = [
    path("", MainPageView.as_view(), name="main"),
]

app_dashboard_urls: list = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/employees", EmployeesView.as_view(), name="employees"),
    path("dashboard/main_panel", MainPanelView.as_view(), name="main_panel"),
    path("dashboard/attendance", AttendanceView.as_view(), name="attendance"),
    path("dashboard/vacation", VacationView.as_view(), name="vacation"),
    path("dashboard/working", WorkingView.as_view(), name="working"),
    path("dashboard/charts", ChartsView.as_view(), name="charts"),
    path("dashboard/emails", EmailView.as_view(), name="emails"),
    path("dashboard/other", OtherView.as_view(), name="other"),
    path("dashboard/sick", SickView.as_view(), name="sick"),
]

app_accounts_urls: list = [
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += app_main_urls
urlpatterns += app_dashboard_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += app_accounts_urls
