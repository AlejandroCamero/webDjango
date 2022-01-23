from ast import Delete
from asyncio.windows_events import NULL
import datetime
from logging import NullHandler
from queue import Empty
from django.http.response import Http404
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView

from django.db.models import Q

from django.urls.base import reverse_lazy

from .models import Category, Employee, Project,Participate,Client

from .forms import ProjectForm, UserForm

# Create your views here.

def index(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        print(username)
        print(password)
        if user:
            login(request,user)
            messages.success(request,"Welcome {}! ".format(user.username))
            return redirect('index')
        else:
            messages.error(request,"Username or password incorrect")
        
    form=UserForm()
    return render(request,'index.html',{"form":form})

class HomePageView(TemplateView):
    template_name="index.html"

class AboutView(TemplateView):
    template_name="plantilla/about.html"
    
class SamplePostView(TemplateView):
    template_name="plantilla/post.html"

class ContactView(TemplateView):
    template_name="plantilla/contact.html"
    
def AllProjectList(request):
    project = Project.objects.filter(Q(finDate="0001-01-01"))
    print(project)
    categories=Category.objects.all()
    return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})

def project(request):
    print(request.GET["categorie"])
    # categories=Category.objects.all()
    # return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})
    
def MyClientProjects(request):
    participates = Participate.objects.filter(idClient__idUser__id=request.user.id).filter(~Q(idProject__finDate="0001-01-01")).order_by('-enrollmentDate')
    return render(request,'nucleo/Myproject_list.html',{'object_list':participates})

def MyEmployeeProjects(request):
    project = Project.objects.filter(~Q(finDate="0001-01-01")).filter(idEmployee__idUser__id=request.user.id).order_by('-initDate')
    return render(request,'nucleo/project_list.html',{'object_list':project})
    
def InscribeClient(request,pk):
    client = Client.objects.get(idUser__id=request.user.id)
    project=Project.objects.get(pk=pk)
    if(project.finDate<datetime.date.today()):
        participate = Participate(idClient=client,idProject=Project.objects.get(pk=pk),enrollmentDate=datetime.date.today(),role="Cliente")
        participate.save()
        messages.add_message(request, messages.INFO, 'Cliente inscrito')
    else:
        messages.add_message(request, messages.INFO, 'El proyecto finalizó. No se pudo inscribir')
    return redirect('AllProjects')
    
    
def ProjectList(request):
    project = Project.objects.filter(idEmployee__idUser__id=request.user.id).filter(Q(finDate="0001-01-01")).order_by('-initDate')
    print(project)
    return render(request,'nucleo/project_list.html',{'object_list':project})

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm

def ProjectUpdate2(request,pk):
    Project.objects.filter(pk=pk).update(finDate=datetime.date.today())
    messages.add_message(request, messages.INFO, 'Proyecto actualizado.')
    return redirect('projects')
    
class ProjectUpdate(UpdateView):
    model=Project
    form_class = ProjectForm
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto actualizado.')
        return reverse_lazy('projects')