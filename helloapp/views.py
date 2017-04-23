from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.middleware import RemoteUserMiddleware

def index(request):
    return HttpResponse("Hello, world")

@login_required(login_url='/login/')
def home(request):
    return render(request,"home.html")

def myurl(request):
    return HttpResponse("Your IP Adress is %s" % request.META['REMOTE_USER']) 

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request,"home.html")
    return render(request, 'login.html')

class RemoteUserMiddleware(object):
    header = "REMOTE_USER"
    def process_request(self, request):
        if not hasattr(request, 'user'):
             raise ImproperlyConfigured(
                 "The django-webtest auth middleware requires the "
                 "'django.contrib.auth.middleware.AuthenticationMiddleware' "
                 "to be installed. Add it to your MIDDLEWARE_CLASSES setting "
                 "or disable django-webtest auth support "
                 "by setting 'setup_auth' property of your WebTest subclass "
                 "to False."
                 )
        try:
            username = request.META[self.header]
        except KeyError:
            return
        if request.user.is_authenticated():
            if request.user.username == self.clean_username(username, request)
                return
        user = auth.authenticate(remote_user=username)
        if user:
            request.user = user
            auth.login(request, user)
            
    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError: # Backend has no clean_username method.
