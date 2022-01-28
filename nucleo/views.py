from asyncio.windows_events import NULL
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator

from django.db.models import Q

from django.urls.base import reverse_lazy

from .models import Category, Employee, Project,Participate,Client
from registration.decorators import same_project_employee
from .forms import ProjectForm, ProjectFormUpdate, UserForm

# BASIC TEMPLATES.

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

# OTHER VIEWS

def AllProjectList(request):
    project = Project.objects.all().order_by('-initDate')
    categories=Category.objects.all()
    participa= Participate.objects.filter(idClient__idUser__id = request.user.id)
    participa_id_list= list()
    for p in participa:
        participa_id_list.append(p.idProject.id)
    return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories, 'participa':participa_id_list})

def project(request):
    print(request.GET["categorie"])
    # categories=Category.objects.all()
    # return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})


def InscribeClient(request,pk):
    client = Client.objects.get(idUser__id=request.user.id)
    project = Project.objects.get(pk=pk)
    if(project.finDate > datetime.date.today()):
        participate = Participate(idClient=client,idProject=Project.objects.get(pk=pk),enrollmentDate=datetime.date.today(),role="Cliente")
        participate.save()
        messages.add_message(request, messages.INFO, 'Cliente inscrito')
    else:
        messages.add_message(request, messages.WARNING, 'El proyecto finalizó. No se pudo inscribir')
    return redirect('AllProjects')

# PROYECTOS FINALIZADOS CLIENTE

def MyClientProjects(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    participates = Participate.objects.filter(idClient__idUser__id=request.user.id).filter(idProject__finDate__lt=now).order_by('-enrollmentDate')
    return render(request,'nucleo/Myproject_list.html',{'object_list':participates})

# PROYECTOS FINALIZADOS DE EMPLEADO

def MyEmployeeProjects(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    project = Project.objects.filter(finDate__lt=now).filter(idEmployee__idUser__id=request.user.id).order_by('finDate')
    return render(request,'nucleo/project_list.html',{'object_list':project})

# CRUD PROJECTS
    
def ProjectList(request):
    projects = Project.objects.all().order_by('-initDate')
    print(projects)
    return render(request,'nucleo/project_list.html',{'object_list':projects})

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto creado.')
        return reverse_lazy('projects')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            employee = Employee.objects.get(idUser = request.user.id)
            project.idEmployee = employee
            project.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

@method_decorator(same_project_employee, name='dispatch')
class ProjectDelete(DeleteView):
    model = Project
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto eliminado.')
        return reverse_lazy('projects')
    

@method_decorator(same_project_employee, name='dispatch')
class ProjectUpdate(UpdateView):
    model=Project
    form_class = ProjectFormUpdate
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto actualizado.')
        return reverse_lazy('projects')