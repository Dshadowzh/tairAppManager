# -*- coding: utf-8 -*-
from django.contrib import admin
from tairAppManager.cluster.models import *

class ClusterAdmin(admin.ModelAdmin):
  search_fields = ['cluster_name']

class GroupAdmin(admin.ModelAdmin):
  search_fields = ['name']

#class DistribAdmin(admin.ModelAdmin):
#  pass

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Group, GroupAdmin)
#admin.site.register(Distrib, DistribAdmin)
