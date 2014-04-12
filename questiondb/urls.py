from django.conf.urls import patterns, url

from questiondb import views

urlpatterns = patterns(
    '',
    # Maps /qdb/ to page listing rounds.
    url(r'^$', views.index, name='index'),

    url(r'^add_question/?$', views.add_question),
    url(r'^edit_question/(?P<question_id>\d+)/?$', views.edit_question),
    url(r'^list_questions/?$', views.list_questions),
    url(r'^list_all_questions/?$', views.list_all_questions),
    url(r'^list_my_questions/?$', views.list_my_questions),

    url(r'^(?P<round_id>\d+)/?$', views.view_round), 
    url(r'^(?P<round_id>\d+)/edit/?$', views.edit_round), 
    url(r'^(?P<round_id>\d+)/mod/?$', views.mod),
    url(r'^add_round/?$', views.add_round),
    url(r'^list_rounds/?$', views.list_rounds),
    url(r'^delete_round/?$', views.delete_round),
)
