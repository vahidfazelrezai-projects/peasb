from django.conf.urls import patterns, url

from questiondb import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^(?P<round_id>\d+)/$', views.view_round, name='view'), 
)
