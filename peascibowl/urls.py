from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from peascibowl import views
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'peascibowl.views.home', name='home'),
    # url(r'^peascibowl/', include('peascibowl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^qdb/', include('questiondb.urls')),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', views.logout_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password_change/', 'django.contrib.auth.views.password_change'),
    url(r'^password_change_done/', 'django.contrib.auth.views.password_change_done'),
)
