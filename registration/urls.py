
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from registration import views

urlpatterns = [
    path("register",views.ClientCreate.as_view(),name="register"),
    path("login",auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path("detail/client/<int:pk>",views.ClientDetailsView.as_view(template_name='auth/client_detail.html'),name="details"),
]

