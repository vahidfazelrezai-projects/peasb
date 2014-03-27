from django.conf.urls import patterns, url

from questiondb import views

urlpatterns = patterns(
    '',
    # Maps /qdb/ to page listing rounds.
    url(r'^$', views.index, name='index'),
    # Maps urls of the form /qdb/round_id to page displaying the round.
    url(r'^(?P<round_id>\d+)/?$', views.view_round), 
    url(r'^add_round/?$', views.add_round),
    url(r'^add_question/?$', views.add_question),
    url(r'^view_questions/?$', views.view_questions),
    url(r'^delete_round/?$', views.delete_round),
)
