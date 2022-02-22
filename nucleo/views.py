import datetime
from io import BytesIO
from msilib import Table
from tkinter.ttk import Style
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator

from django.views import View

from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from webDjango import settings

from .models import Client


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

class PDFGenerator(View):
    
    global style
    style = getSampleStyleSheet()
    styleN = style['Normal']
    width, height = pagesizes.A4
    
    def header(self,cliente_pdf):
        
        cliente_pdf.setFillColorRGB(0.3,0.3,0.3)
        cliente_pdf.rect(0,780,800,100, fill=1)
        cliente_pdf.setFillColorRGB(1,1,1)
        cliente_pdf.setFont('Helvetica',20)
        cliente_pdf.drawString(10,800, "Easy Project")
        
        cliente_pdf.setFont('Helvetica-Bold',25)
        cliente_pdf.setFillColorRGB(0,0,0)
        cliente_pdf.drawString(150,740, u"INFORME DE PROYECTOS")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0,0,0)
        cliente_pdf.drawString(10,700, u"DATOS DE CLIENTE")
        
        cliente_pdf.setFont('Times-Roman',17)
        cliente_pdf.setFillColorRGB(0,0,0)
        cliente_pdf.drawString(10,580,u"PROYECTOS EN LOS QUE PARTICIPA EL CLIENTE")
        
    def table_datos_cliente(self,cliente_pdf,posicion_y,cliente_id):
        encabezado = ['DNI','Nombre','Apellidos','Dirección']
        datos = [(cliente_id.dni,cliente_id.name,cliente_id.surname,cliente_id.address)]
        datos_orden = Table([encabezado]+ datos, colWidths=[4*cm,4*cm,4*cm, 5*cm])
        datos_orden.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(3,4),'CENTER'),
                ('GRID',(0,0),(-1,-1), 1,colors.black),
                ('FONTSIZE',(0,0),(-1,-1),10),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(red=(250/255),green=(128/255),blue=(114/255),alpha=(125/255))),
                ('BACKGROUND',(0,1),(-1,1),colors.Color(red=(102/255),green=(216/255),blue=(238/255),alpha=(125/255))),
            ]
        ))
        
        datos_orden.wrapOn(cliente_pdf,self.width,self.height)
        datos_orden.drawOn(cliente_pdf,10,posicion_y)
        return datos_orden
    
    def Para(self,txt):
        return Paragraph(txt, self.styleN)
        
    
    def table_datos_proyecto(self,cliente_pdf,posicion_y,participates):
        encabezado = ['Título','Descripción','Inicio','Fin', 'Nivel','Categoría','Informe']
        datos = [
            (
                self.Para(self, p.idProject.title),
                self.Para(self, p.idProject.description),
                self.Para(self, p.idProject.initDate.strftime("%d/%m/%Y")),
                self.Para(self, p.idProject.finDate.strftime("%d/%m/%Y")),
                self.Para(self, str(p.idProject.level)),
                self.Para(self, p.idProject.idCategory.name),
                self.Para(self, str(p.idProject.report))
            ) for p in participates
        ]
        datos_pry = Table([encabezado]+datos, colWidths=[3*cm, 4*cm, 2.25*cm, 2.25*cm, 1*cm, 2.5*cm, 5*cm], rowHeights=(len(datos)+1)*[1*cm],splitByRow=True)
        datos_pry.setStyle(TableStyle(
            [
                ('ALIGN',(0,0),(7,0),'CENTER'),
                ('GRID',(0,0),(-1,-1),0.5, colors.black),
                ('FONTSIZE',(0,0),(-1,-1),10),
                ('BACKGROUND',(0,0),(-1,0),colors.Color(red=(250/255),green=(128/255),blue=(114/255),alpha=(125/255))),
            ]
        ))
        posicion_y = posicion_y - (len(datos)+1)*(1*cm)
        
        datos_pry.wrapOn(cliente_pdf,self.width,self.height)
        datos_pry.drawOn(cliente_pdf,10,posicion_y)
        return datos_pry
    
    def gen_pdf(self, request, initDate, finDate):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe_cliente.pdf"'
        
        buffer = BytesIO()
        cliente_pdf=canvas.Canvas(buffer,pagesize=pagesizes.A4)
        cliente_pdf.setTitle('Informe de cliente')
        
        self.header(self, cliente_pdf)
        id_cliente = Client.objects.filter(idUser=request.user.id).first()
        posicion_cliente_y=640
        self.table_datos_cliente(self, cliente_pdf, posicion_cliente_y, id_cliente)
        
        participates = Participate.objects.filter(idClient__idUser__id=request.user.id).filter(idProject__initDate__gt = initDate).filter(idProject__initDate__lt = finDate).order_by('idProject__initDate')
        posicion_proyectos_y=550
        self.table_datos_proyecto(self, cliente_pdf, posicion_proyectos_y, participates)
        
        cliente_pdf.showPage()
        cliente_pdf.save()
        
        cliente_pdf = buffer.getvalue()
        buffer.close()
        response.write(cliente_pdf)
        
        return response
        
@client_is_active
def informe_pdf(request):
    initDate = request.POST['fecha_ini']
    finDate = request.POST['fecha_fin']
    if initDate != None and initDate != '' and finDate != None and initDate != '' and initDate < finDate:
        pdf = PDFGenerator
        return pdf.gen_pdf(pdf ,request, initDate, finDate)
    else:
        messages.add_message(request, messages.ERROR, 'Las fechas no son válidas')
        return HttpResponseRedirect('/nucleo/clientProjects')