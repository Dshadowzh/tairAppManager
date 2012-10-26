# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('tairAppManager.cluster', 
  (r'^$','views.getAllCluster'),
  (r'^(?P<group_id>\d+)/$','views.getCluster'),
  (r'^(?P<group_id>\d+)/ns$','views.getUnusedNamespace'),
  (r'^(?P<group_id>\d+)/nscheck$','views.checkNamespace'),
  (r'^(?P<group_id>\d+)/app$','views.getApps'),
  (r'^(?P<group_id>\d+)/manage$','views.getManger'),
  (r'^(?P<group_id>\d+)/node$','views.getNodes'),
  (r'^test$','views.getTest'),
#  (r'^alloc$','tair.rAllocNamespaceAuto'),
#  (r'^alloc2$','tair.rAllocNamespace'),
#  (r'^modify$','tair.rSetQuota'),
)
