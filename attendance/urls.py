"""URLs"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from accounts.views import (
    CustomLoginView,
    SignUpView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    user_logout,
)
from app_dashboard.views import (
    AttendanceView,
    CamView,
    ChartsView,
    CreateEmpView,
    DepartmentDetailList,
    DepartmentListView,
    EmailView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeesView,
    EmployeeUpdateView,
    EmpStatusDetailList,
    MainPanelView,
    RedirectDashboard,
    SaveVectorToDbView,
    StatusView,
    TakeVectorView,
)
from app_main.views import (
    CamStreamView,
    CheckPinView,
    ComparePinView,
    EmpLoginView,
    GetResultView,
    MainPageView,
    SetStatusView,
)

urlpatterns = [
    path("", RedirectDashboard.as_view()),
    path("admin/", admin.site.urls),
    path("camstream/<int:speed>", CamStreamView.as_view(), name="camstream"),
]

app_dashboard_urls: list = [
    path("dashboard/main_panel", MainPanelView.as_view(), name="main_panel"),
    path(
        "dashboard/save_vector_to_db/<slug:slug>",
        SaveVectorToDbView.as_view(),
        name="save_vector_to_db",
    ),
    path(
        "dashboard/take_vector/<slug:slug>/",
        TakeVectorView.as_view(),
        name="take_vector",
    ),
    path("dashboard/create_emp", CreateEmpView.as_view(), name="create_emp"),
    path("dashboard/employees", EmployeesView.as_view(), name="employees"),
    path(
        "dashboard/detail_employee/<slug:slug>/",
        EmployeeDetailView.as_view(),
        name="detail_employee",
    ),
    path(
        "dashboard/delete_employee/<slug:slug>/",
        EmployeeDeleteView.as_view(),
        name="delete_employee",
    ),
    path(
        "dashboard/update_employee/<slug:slug>/",
        EmployeeUpdateView.as_view(),
        name="update_employee",
    ),
    path("dashboard/emails", EmailView.as_view(), name="emails"),
    path("dashboard/attendance", AttendanceView.as_view(), name="attendance"),
    path("dashboard/charts", ChartsView.as_view(), name="charts"),
    path(
        "dashboard/department_list/",
        DepartmentListView.as_view(),
        name="department_list",
    ),
    path(
        "dashboard/department_detail_list/<int:pk>",
        DepartmentDetailList.as_view(),
        name="department_detail_list",
    ),
    path(
        "dashboard/emp_status_detail_list/<int:pk>",
        EmpStatusDetailList.as_view(),
        name="emp_status_detail_list",
    ),
    path("dashboard/cam<int:speed>", CamView.as_view(), name="cam"),
    path("dashboard/status", StatusView.as_view(), name="status"),
]

app_main_urls: list = [
    path("app_main/<int:speed>", MainPageView.as_view(), name="mainpage"),
    path("app_main/get_result", GetResultView.as_view(), name="get_result"),
    path(
        "app_main/check_pin/<slug:slug>",
        CheckPinView.as_view(),
        name="check_pin",
    ),
    path("app_main/compare_pin", ComparePinView.as_view(), name="compare_pin"),
    path(
        "app_main/emp_login/<slug:slug>",
        EmpLoginView.as_view(),
        name="emp_login",
    ),
    path("app_main/set_status", SetStatusView.as_view(), name="set_status"),
]

app_accounts_urls: list = [
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", user_logout, name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/user_list/", UserListView.as_view(), name="user_list"),
    path(
        "accounts/user/<int:pk>/", UserDetailView.as_view(), name="user_detail"
    ),
    path(
        "accounts/delete-user/<int:pk>/",
        UserDeleteView.as_view(),
        name="delete-user",
    ),
    path(
        "accounts/update-user/<int:pk>/",
        UserUpdateView.as_view(),
        name="update-user",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += app_dashboard_urls
urlpatterns += app_main_urls
urlpatterns += app_accounts_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
