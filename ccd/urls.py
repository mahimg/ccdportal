from django.conf.urls import url

from . import views

app_name = 'ccd'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^studentDetails/(?P<rollNo>[a-zA-Z0-9-]+)/$', views.studentDetails, name='studentDetails'),
    url(r'^updateStateMain/$', views.updateStateMain, name='updateStateMain'),
    url(r'^updateRequestState/$', views.updateRequestState, name='updateRequestState'),
    url(r'^search/$', views.search, name='search'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^uploadData/$', views.uploadData, name='uploadData'),
    url(r'^login/$', views.loginUser, name='login'),
    url(r'^logout/$', views.logoutUser, name='logout'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),
    url(r'^uploadModelFile/$', views.uploadModelFile, name='uploadModelFile'),
    url(r'^contact/$', views.contact, name='contact'),
]
