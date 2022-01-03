
from django.contrib import admin
from django.urls import path
from registration import views

urlpatterns = [
    path("register",views.register,name="register")
]

    