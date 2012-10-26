# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('tairAppManager.api', 
  (r'^area/(?P<area_key>\w+)$','api.area'),
  #(r'^cluster/(?P<cluster_id>\d+$','api.cluster'),
  #(r'^node/(?P<node_id>\d+$','api.node'),
)
