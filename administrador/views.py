from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.http.response import  HttpResponseRedirect

from .forms import ClientForm,EmployeeForm, UserCreationFormWithEmail
from nucleo.models import Client,Employee


class ClientCreate(CreateView):
    form_class = ClientForm
    second_form_class = UserCreationFormWithEmail
    template_name = 'nucleo/client_form.html'
    
    def get_success_url(self):
        return reverse_lazy('clients')+'?register'
    
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
    second_form_class = UserCreationFormWithEmail
    template_name = 'nucleo/employee_form.html'
    
    def get_success_url(self):
        return reverse_lazy('employees')+'?register'
    
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
