# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.views import login as auth_login
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url



#def index(request):
#    return HttpResponse("Hello, world")

@login_required(login_url='/login/')
def home(request):
    return render(request,"home.html")

def myurl(request):
    return HttpResponse("Your username is %s" % request.META['REMOTE_USER']) 

def index(request):
    activity_list = User.objects.order_by('-last_login')[:20]
    user_groups = request.user.groups.values_list('name', flat=True)
    user_permissions = request.user.get_all_permissions()
    context = {
        'user': request.user,
        'user_groups': user_groups,
        'user_permissions': user_permissions,
        'activity_list': activity_list,
    }
    return render(request, 'index.html', context)


def login(request, template_name='login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    if hasattr(request, 'user') and request.user.is_authenticated():
        redirect_to = request.POST.get(redirect_field_name,
            request.GET.get(redirect_field_name, ''))
        if not is_safe_url(url=redirect_to, host=request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect(redirect_to)
    return auth_login(request, template_name = template_name, redirect_field_name = redirect_field_name)
