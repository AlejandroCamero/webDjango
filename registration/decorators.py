from django.http.response import  HttpResponseRedirect
from nucleo.models import User, Client, Employee, Project
from django.contrib import messages

def same_user(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        if not (user.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def same_client(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        client = Client.objects.get(pk=pk)
        if not (client.idUser.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def same_employee(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        employee = Employee.objects.get(pk=pk)
        if not (employee.idUser.id + " " + request.user.id):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def same_project_employee(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        project = Project.objects.get(pk=pk)
        if not (project.idEmployee.idUser.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def is_employee(func):
    def check_and_call(request, *args, **kwargs):
        if not (request.user.is_staff and not request.user.is_superuser):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def is_client(func):
    def check_and_call(request, *args, **kwargs):
        if request.user.is_staff:
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def client_is_active(func):
    def check_and_call(request, *args, **kwargs):
        client = Client.objects.get(idUser__id=request.user.id)
        if not client.active:
            messages.add_message(request, messages.ERROR, 'El cliente no está activado.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

def is_admin(func):
    def check_and_call(request, *args, **kwargs):
        if not (request.user.is_staff and request.user.is_superuser):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call

