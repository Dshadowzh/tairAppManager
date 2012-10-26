# -*- coding: utf-8 -*-
from django.contrib import admin
from tairAppManager.node.models import Node

class NodeAdmin(admin.ModelAdmin):
  pass

admin.site.register(Node, NodeAdmin)
