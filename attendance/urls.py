"""URLs"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from accounts.views import CustomLoginView, user_logout
from app_dashboard.views import (
    AttendanceView,
    CamView,
    ChartsView,
    DashboardView,
    EmailView,
    EmployeesView,
    MainPanelView,
    OtherView,
    RedirectDashboard,
    SickView,
    VacationView,
    WorkingView,
)
from app_main.views import CamStreamView, GetResultView, MainPageView

urlpatterns = [
    path("", RedirectDashboard.as_view()),
    path("admin/", admin.site.urls),
    path("camstream/<int:speed>", CamStreamView.as_view(), name="camstream"),
]

app_dashboard_urls: list = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/attendance", AttendanceView.as_view(), name="attendance"),
    path("dashboard/main_panel", MainPanelView.as_view(), name="main_panel"),
    path("dashboard/employees", EmployeesView.as_view(), name="employees"),
    path("dashboard/vacation", VacationView.as_view(), name="vacation"),
    path("dashboard/working", WorkingView.as_view(), name="working"),
    path("dashboard/cam<int:speed>", CamView.as_view(), name="cam"),
    path("dashboard/charts", ChartsView.as_view(), name="charts"),
    path("dashboard/emails", EmailView.as_view(), name="emails"),
    path("dashboard/other", OtherView.as_view(), name="other"),
    path("dashboard/sick", SickView.as_view(), name="sick"),
]

app_main_urls: list = [
    path("app_main/<int:speed>", MainPageView.as_view(), name="mainpage"),
    path("app_main/get_result", GetResultView.as_view(), name="get_result"),
]

app_accounts_urls: list = [
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", user_logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += app_dashboard_urls
urlpatterns += app_main_urls
urlpatterns += app_accounts_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
