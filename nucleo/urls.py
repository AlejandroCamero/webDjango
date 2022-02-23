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
    path('homePage', views.HomePageView.as_view(),name="homePage"),
    path('about', views.AboutView.as_view(),name="about"),
    path('samplePost', views.SamplePostView.as_view(),name="samplePost"),
    path('contact', views.ContactView.as_view(),name="contact"),
    path('', views.index,name="index"),
    
    path('AllProjects',views.AllProjectList,name="AllProjects"),
    path('projectCreate',views.ProjectCreate.as_view(),name="projectCreate"),
    path('projectBaja/<int:pk>',views.ProjectDelete.as_view(),name="projectDelete"),
    path('projectUpdate/<int:pk>',views.ProjectUpdate.as_view(),name="projectUpdate"),
    path('projectFinal/<int:pk>',views.ProjectReportUpdate.as_view(),name="projectFinal"),
    path('projectClients/<int:pk>',views.projectClients,name="projectClients"),
    path('roleAsignment/<int:pk>',views.UpdateRole.as_view(),name="roleAsignment"),
    path('clientProjects',views.MyClientProjects,name="MyClientProjects"),
    path('employeeProjects',views.MyEmployeeProjects,name="MyEmployeeProjects"),
    path('inscribe/<int:pk>',views.InscribeClient,name="inscribe"),
    
    path('informe_pdf',views.informe_pdf,name="informe_pdf"),
    
    path('api/token',views.LoginView.as_view()),
    path('api/myprojects/<int:pk>',views.Project_APIView.as_view(),name="api"),
    
    
]
