from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^process/$', views.process,name="process"),
    url(r'^login/$', views.login,name="login"),
    url(r'^dashboard/$', views.dashboard,name="dashboard"),
    url(r'^create/$', views.create,name="create"),
    url(r'^create_wish/$', views.create_wish,name="create_wish"),
    url(r'^(?P<id>\d+)/edit/$', views.edit,name="edit"),
    url(r'^(?P<id>\d+)/update/$', views.update,name="update"),
    url(r'^(?P<id>\d+)/destroy/$', views.destroy,name="destroy"),
    url(r'^(?P<id>\d+)/grant/$', views.grant,name="grant"),
    url(r'^(?P<id>\d+)/like/$', views.like,name="like"),
    url(r'^stats/$', views.stats,name="stats"),
    url(r'^logout/$', views.logout,name="logout"),
]