# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from tairAppManager.cluster.views import *
from tairAppManager.app.views import *
from django.conf import settings
#tmp
from django.views.generic.base import TemplateView

#admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tairAppManager.app.views.getAllApp'),
    url(r'^app/', include('tairAppManager.app.urls')),
    url(r'^cluster/', include('tairAppManager.cluster.urls')),
    url(r'^message/', include('tairAppManager.message.urls')),
    url(r'^openapi/', include('tairAppManager.api.urls')),
    url(r'^feedback', 'tairAppManager.app.helper.feedback'),
    #url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$',  login),
    url(r'^accounts/logged_out/$', logout),
)

#if settings.DEBUG:
#    urlpatterns += patterns('django.contrib.staticfiles.views', url(r'^static/(?P<path>.*)$', 'serve'))
