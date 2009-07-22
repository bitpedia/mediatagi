from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djmediatagi/', include('djmediatagi.foo.urls')),
    (r'^bzpull/@(?P<target>.*)', 'djmediatagi.tvents.views.bzpull'),
    (r'^log(/(?P<tag>.*))?', 'djmediatagi.tvents.views.log'),
    (r'^summary(/(?P<tag>.*))?', 'djmediatagi.tvents.views.summary'),
    (r'^$', 'djmediatagi.tvents.views.home'),
    (r'^addtags(/@(?P<target_id>.*))?', 'djmediatagi.tvents.views.addtags'),                       

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

import settings

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^s/(?P<path>.*)$', 'serve', {'document_root': '/home/mediatagi/django/s/',
                                                   'show_indexes': True }),)


        
