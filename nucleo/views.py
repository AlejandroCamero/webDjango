import datetime
from io import BytesIO
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator

from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


from django.urls.base import reverse_lazy

from .models import Category, Employee, Project,Participate,Client
from registration.decorators import same_project_employee, is_employee, is_client, client_is_active, same_project_participant
from .forms import ProjectForm, ProjectFormUpdate, UserForm, ParticipateRoleUpdateForm,ProjectReportFormUpdate
from.constants import ROLES

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

@is_client
@client_is_active
def InscribeClient(request,pk):
    client = Client.objects.get(idUser__id=request.user.id)
    project = Project.objects.get(pk=pk)
    if(project.finDate > datetime.date.today()):
        if (Participate.objects.filter(idClient__id = client.id).filter(idProject__id = project.id) ):
            messages.add_message(request, messages.ERROR, 'El cliente ya está inscrito en ese proyecto.')
        else:
            participate = Participate(idClient=client,idProject=project,enrollmentDate=datetime.date.today())
            participate.save()
            messages.add_message(request, messages.INFO, 'Cliente inscrito')
    else:
        messages.add_message(request, messages.ERROR, 'El proyecto finalizó. No se pudo inscribir.')
    return redirect('AllProjects')

# PROYECTOS FINALIZADOS CLIENTE

@is_client
def MyClientProjects(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    participates = Participate.objects.filter(idClient__idUser__id=request.user.id).order_by('-enrollmentDate')
    return render(request,'nucleo/Myproject_list.html',{'object_list':participates})

# PROYECTOS FINALIZADOS DE EMPLEADO

@is_employee
def MyEmployeeProjects(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    project = Project.objects.filter(is_finalized=True).filter(idEmployee__idUser__id=request.user.id).order_by('finDate')
    return render(request,'nucleo/Myproject_list.html',{'object_list':project})

# CRUD PROJECTS
def AllProjectList(request):
    now = datetime.datetime.today().date()
    if (request.method == "GET"):
        if (request.user.is_staff):
            project = Project.objects.filter(is_finalized=False).filter(idEmployee__idUser__id=request.user.id).order_by('-initDate')
        else:
            project = Project.objects.filter(is_finalized=False).order_by('-initDate')
        categories=Category.objects.all()
        return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories, 'now':now})
    else:
        idCat = request.POST.get('categorie', False)
        if (idCat == "0"):
            if (request.user.is_staff):
                project = Project.objects.filter(is_finalized=False).filter(idEmployee__idUser__id=request.user.id).order_by('-initDate')
            else:
                project = Project.objects.all().order_by('-initDate')
            categories=Category.objects.all()
            return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})
        elif (idCat == "-1"):
            if(not request.user.is_staff):
                date = datetime.datetime.today()
                week = date.strftime("%V")
                week = int(week) + 1
                project = Project.objects.filter(is_finalized=False).filter(initDate__week = week).order_by('-initDate')
                categories=Category.objects.all()
                return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})
            else:
                messages.add_message(request, messages.ERROR, 'Acción no permitida.')
                project = Project.objects.filter(is_finalized=False).filter(idEmployee__idUser__id=request.user.id).order_by('-initDate')
                categories=Category.objects.all()
                return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})
        else:
            if (request.user.is_staff):
                project = Project.objects.filter(is_finalized=False).filter(idCategory__id = idCat).filter(idEmployee__idUser__id=request.user.id).order_by('-initDate')
            else:
                project = Project.objects.filter(idCategory__id = idCat).order_by('-initDate')
            categories=Category.objects.all()
            return render(request,'nucleo/project_list.html',{'object_list':project,'categories':categories})

@method_decorator(is_employee, name='dispatch')
class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto creado.')
        return reverse_lazy('AllProjects')
    
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
        return reverse_lazy('AllProjects')
    

@method_decorator(same_project_employee, name='dispatch')
class ProjectUpdate(UpdateView):
    model=Project
    form_class = ProjectFormUpdate
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto actualizado.')
        return reverse_lazy('AllProjects')
    
@method_decorator(same_project_employee, name='dispatch')
class ProjectReportUpdate(UpdateView):
    model=Project
    form_class = ProjectReportFormUpdate
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Proyecto actualizado.')
        return reverse_lazy('MyEmployeeProjects')
    
    def post(self, request, *args, **kwargs):
        pk=kwargs['pk']
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            project = Project.objects.filter(pk = pk).first()
            project.finDate= datetime.datetime.now().strftime('%Y-%m-%d')
            project.is_finalized=True
            project.report = form.cleaned_data['report']
            project.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        

@same_project_employee
def projectClients(request, pk):
    project = Project.objects.filter(pk = pk).first()
    if (request.method == "GET"):
        participates = Participate.objects.all().filter(idProject = project)
        return render(request,'nucleo/project_clients.html',{'object_list':participates, 'project':project, 'roles': ROLES})
    else:
        role = request.POST.get('role', False)
        if (role == "0"):
            participates = Participate.objects.all().filter(idProject = project)
            return render(request,'nucleo/project_clients.html',{'object_list':participates, 'project':project, 'roles': ROLES})
        else:
            participates = Participate.objects.filter(idProject = project).filter(role=role)
            return render(request,'nucleo/project_clients.html',{'object_list':participates, 'project':project, 'roles': ROLES})
        

@method_decorator(same_project_participant, name='dispatch')
class UpdateRole(UpdateView):
    form_class = ParticipateRoleUpdateForm
    model = Participate
    template_name = 'nucleo/role_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rol actualizado.')
        return reverse_lazy('AllProjects')  

# GENERAR PDF

@client_is_active
def informe_pdf(request):
    initDate = request.POST['fecha_ini']
    finDate = request.POST['fecha_fin']
    if initDate != None and initDate != '' and finDate != None and initDate != '' and initDate < finDate:
        return gen_pdf(request, initDate, finDate)
    else:
        messages.add_message(request, messages.ERROR, 'Las fechas no son válidas')
        return HttpResponseRedirect('/nucleo/clientProjects')


def gen_pdf(request, initDate, finDate):
    buffer=BytesIO()
    pdf = canvas.Canvas(buffer,pagesize=letter,bottomup=0)
    textob=pdf.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    
    participates = Participate.objects.filter(idClient__idUser__id=request.user.id).filter(idProject__finDate__gt = initDate).filter(idProject__finDate__lt = finDate).order_by('-enrollmentDate')
    
    lines=[]
    
    for participate in participates:
        lines.append(participate)
    
    for participate in participates:
        textob.textLine("Proyecto: " + participate.idProject.title)
        textob.textLine("- Descripcion: " + participate.idProject.description)
        textob.textLine("- Nivel: " + str(participate.idProject.level))
        textob.textLine("- Fecha de Inicio: " + str(participate.idProject.initDate))
        textob.textLine("- Fecha final: " + str(participate.idProject.finDate))
        textob.textLine("- Categoria: " + participate.idProject.idCategory.name)
        if not participate.idProject.report == None:
            textob.textLine("- Reporte: " + participate.idProject.report)
        else:
            textob.textLine("- Reporte: N/D")
        textob.textLine("")
            
    pdf.drawText(textob)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True,filename='informe.pdf')