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
from . import views

urlpatterns = [
    # path('employees', views.ListView.as_view(),name="employees"),
    path('clients', views.ClientList.as_view(),name="clients"),
    path('clientDelete/<int:pk>', views.ClientDelete.as_view(),name="clientDelete"),
    path('clientActivate/<int:pk>', views.ClientActivate,name="clientActivate"),
    path('clientDesactivate/<int:pk>', views.ClientDesactivate,name="clientDesactivate"),
    path('clientCreate', views.ClientCreate.as_view(),name="clientCreate"),
    
    path('employees', views.EmployeeList.as_view(),name="employees"),
    path('employeeDelete/<int:pk>', views.EmployeeDelete.as_view(),name="employeeDelete"),
    path('employeeCreate', views.EmployeeCreate.as_view(),name="employeeCreate"),
]
