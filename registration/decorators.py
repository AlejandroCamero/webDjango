from django.http.response import  HttpResponseRedirect
from nucleo.models import User, Client

def same_user(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        if not (user.id == request.user.id):
            return HttpResponseRedirect('/nucleo/?forbidden')
        return func(request, *args, **kwargs)
    return check_and_call

def same_client(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        client = Client.objects.get(pk=pk)
        if not (client.idUser.id == request.user.id):
            return HttpResponseRedirect('/nucleo/?forbidden')
        return func(request, *args, **kwargs)
    return check_and_call