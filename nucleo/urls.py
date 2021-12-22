"""webDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nucleo import views

urlpatterns = [
    path('/homePage', views.HomePageView.as_view(),name="homePage"),
    path('/', views.index,name="index"),
    path('/users',views.users,name="users"),
    path('/usersView',views.UsersView.as_view(),name="usersView"),
    path('/users/<int:user_id>',views.usersDetails,name="user"),
    path('/usersDetail/<pk>',views.UserDetails.as_view(),name="userDetails"),
]
