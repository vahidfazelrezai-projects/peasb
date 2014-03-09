from django.conf.urls import patterns, url

from questiondb import views

urlpatterns = patterns('',
    # Maps / to page listing rounds.
    url(r'^$', views.index, name='index'),
    # Maps urls of the form .../round_id to page displaying the round.
    url(r'^(?P<round_id>\d+)/$', views.view_round, name='view'), 
)
