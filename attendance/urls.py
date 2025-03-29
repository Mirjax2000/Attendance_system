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
from API.views import DepartmentApi, EmployeeDetail, EmployeesApi
from app_dashboard import views
from app_dashboard.views import (
    AttendanceView,
    CamView,
    ChartsView,
    CreateDepView,
    CreateEmpView,
    DeleteDepView,
    DepartmentDetailList,
    DepartmentListView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeesView,
    EmployeeUpdateView,
    EmpStatusDetailList,
    FillDbView,
    MainPanelView,
    RedirectDashboard,
    ResetDbView,
    SaveVectorToDbView,
    StatusView,
    TakeVectorView,
    UpdateDepView, MailDepartmentPartialView, MailEmployeePartialView,
    MailManualPartialView, SendMailView,
)
from app_main.views import (
    CamStreamView,
    CheckPinView,
    ComparePinView,
    EmpLoginView,
    GetResultView,
    InfoView,
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
    path('dashboard/send-mail/', SendMailView.as_view(), name='send_mail_view'),
    path('dashboard/mail-manual-partial/', MailManualPartialView.as_view(),
         name='mail_manual_partial'),
    path('dashboard/mail-employee-partial/', MailEmployeePartialView.as_view(),
         name='mail_employee_partial'),
    path('dashboeard/mail-department-partial/', MailDepartmentPartialView.as_view(),
         name='mail_department_partial'),
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
    path("dashboard/create_dep", CreateDepView.as_view(), name="create_dep"),
    path(
        "dashboard/update_dep/<int:pk>",
        UpdateDepView.as_view(),
        name="update_dep",
    ),
    path(
        "dashboard/delete_dep/<int:pk>",
        DeleteDepView.as_view(),
        name="delete_dep",
    ),
    path(
        "dashboard/emp_status_detail_list/<int:pk>",
        EmpStatusDetailList.as_view(),
        name="emp_status_detail_list",
    ),
    path("dashboard/cam<int:speed>", CamView.as_view(), name="cam"),
    path("dashboard/status", StatusView.as_view(), name="status"),
    path("dashboard/filldb", FillDbView.as_view(), name="filldb"),
    path("dashboard/resetdb", ResetDbView.as_view(), name="resetdb"),
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
    path("app_main/info/<slug:slug>", InfoView.as_view(), name="info"),
]

app_accounts_urls: list = [
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", user_logout, name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/user_list/", UserListView.as_view(), name="user_list"),
    path("accounts/user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
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
api_urls: list = [
    path("api/employees/", EmployeesApi.as_view(), name="api_employees"),
    path("api/departments/", DepartmentApi.as_view(), name="api_departments"),
    path("api/emp_status/", DepartmentApi.as_view(), name="api_emp_status"),
    path(
        "api/emp_detail/<slug:slug>/",
        EmployeeDetail.as_view(),
        name="api_emp_detail",
    ),
]
urlpatterns += app_dashboard_urls
urlpatterns += app_main_urls
urlpatterns += app_accounts_urls
urlpatterns += api_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
