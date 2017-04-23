from django.conf.urls import  include, url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^myurl/$', views.myurl, name='myurl'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', logout, name='logout', kwargs={'next_page': '/'}),
]
