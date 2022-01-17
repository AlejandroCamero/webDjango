from urllib import response
from django.shortcuts import render

from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy

from .forms import ClientForm,EmployeeForm
from nucleo.models import Client,Employee


class ClientCreate(CreateView):
    form_class = ClientForm
    template_name = 'nucleo/client_form.html'

def ClientActivate(request,pk):
    Client.objects.filter(pk=pk).update(active=1)
    return redirect('clients')

def ClientDesactivate(request,pk):
    Client.objects.filter(pk=pk).update(active=0)
    return redirect('clients')
    
class ClientList(ListView):
    model=Client
    
class ClientDelete(DeleteView):
    model=Client
    success_url=reverse_lazy('clients')


class EmployeeList(ListView):
    model=Employee
    
class EmployeeCreate(CreateView):
    form_class = EmployeeForm
    template_name = 'nucleo/employee_form.html'

class EmployeeDelete(DeleteView):
    model=Employee
    success_url=reverse_lazy('employees')
