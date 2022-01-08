from django.http.response import  HttpResponseRedirect
from nucleo.models import User

def same_user(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        if not (user.id == request.user.id):
            return HttpResponseRedirect('/?forbidden')
        return func(request, *args, **kwargs)
    return check_and_call