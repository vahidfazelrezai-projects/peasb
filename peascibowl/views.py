from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect('/qdb')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

