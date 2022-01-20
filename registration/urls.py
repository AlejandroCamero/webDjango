
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from registration import views

urlpatterns = [
    path("register",views.ClientCreate.as_view(),name="register"),
    path("login",auth_views.LoginView.as_view(),name="login"),
    path("detail/client/<int:pk>",views.ClientDetailsView.as_view(template_name='auth/client_detail.html'),name="details_client"),
    path("detail/employee/<int:pk>",views.EmployeeDetailsView.as_view(template_name='auth/client_detail.html'),name="details_employee"),
    path("update/client/<int:pk>",views.ClientUpdate.as_view(),name="update_client"),
    path("update/employee/<int:pk>",views.EmployeeUpdate.as_view(),name="update_employee"),
    path("update/user/<int:pk>",views.UserUpdate.as_view(),name="updateUser"),
]

