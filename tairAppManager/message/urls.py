# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('tairAppManager.message', 
   (r'^$','views.messageHome'),
   #(r'^(?P<user_id>\d+)$','views.getUserMessage'),
   #(r'^m/(?P<message_id>\d+)$','views.getMessage'),
   #(r'^(?P<apply_id>\d+)/edit/$','views.editApply'),
   #(r'^(?P<apply_id>\d+)/review/$','views.reviewApply'),
)
