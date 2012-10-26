# -*- coding: utf-8 -*-
from django.contrib import admin
from tairAppManager.ssouser.models import MyGroup

class MyGroupAdmin(admin.ModelAdmin):
  pass

admin.site.register(MyGroup, MyGroupAdmin)
