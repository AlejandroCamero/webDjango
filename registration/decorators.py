from django.http.response import  HttpResponseRedirect
from nucleo.models import User, Client, Employee
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
        if not (employee.idUser.id == request.user.id):
            messages.add_message(request, messages.ERROR, 'Acción no permitida.')
            return HttpResponseRedirect('/nucleo/')
        return func(request, *args, **kwargs)
    return check_and_call