from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.http.response import  HttpResponseRedirect

from .forms import ClientForm,EmployeeForm, UserCreationFormWithEmail, CategoryForm
from nucleo.models import Client,Employee, Category

# VISTAS CLIENTES

class ClientCreate(CreateView):
    form_class = ClientForm
    second_form_class = UserCreationFormWithEmail
    template_name = 'nucleo/client_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Cliente creado.')
        return reverse_lazy('clients')
    
    def get_context_data(self, **kwargs):
        context = super(ClientCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            client = form.save(commit=False)
            client.idUser = form2.save()
            client.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

def ClientActivate(request,pk):
    Client.objects.filter(pk=pk).update(active=1)
    messages.add_message(request, messages.INFO, 'Cliente activado.')
    return redirect('clients')

def ClientDesactivate(request,pk):
    Client.objects.filter(pk=pk).update(active=0)
    messages.add_message(request, messages.INFO, 'Cliente desactivado.')
    return redirect('clients')
    
class ClientList(ListView):
    model=Client
    
class ClientDelete(DeleteView):
    model=Client
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Cliente borrado.')
        return reverse_lazy('clients')

# VISTAS EMPLEADO
class EmployeeList(ListView):
    model=Employee
    
class EmployeeCreate(CreateView):
    form_class = EmployeeForm
    second_form_class = UserCreationFormWithEmail
    template_name = 'nucleo/employee_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Empleado creado.')
        return reverse_lazy('employees')
    
    def get_context_data(self, **kwargs):
        context = super(EmployeeCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form2.save(commit=False)
            user.is_staff = True
            user.save()
            client = form.save(commit=False)
            client.idUser = form2.save()
            client.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EmployeeDelete(DeleteView):
    model=Employee
    success_url=reverse_lazy('employees')
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Empleado eliminado.')
        return reverse_lazy('employees')

# VISTAS CATEGORIAS

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'administrador/category_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Categoría creada.')
        return reverse_lazy('categories')


class CategoryList(ListView):
    model=Category
    template_name = 'administrador/category_list.html'


class CategoryUpdate(UpdateView):
    model=Category
    form_class = CategoryForm
    template_name = 'administrador/category_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Categoría actualizada.')
        return reverse_lazy('categories')


class CategoryDelete(DeleteView):
    model=Category
    template_name = 'administrador/category_confirm_delete.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Categoría borrada.')
        return reverse_lazy('categories')
    