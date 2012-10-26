# -*- coding: utf-8 -*-
from django.contrib import admin
from tairAppManager.app.models import * 

class AppAdmin(admin.ModelAdmin):
  search_fields = ['id', 'name']
  ordering = ['-id']

class AppApplyAdmin(admin.ModelAdmin):
  ordering = ['-id']
  pass

class AppReviewAdmin(admin.ModelAdmin):
  search_fields = ['id']
  ordering = ['-id']
  pass

class FeedbackAdmin(admin.ModelAdmin):
  ordering = ['-id']
  pass

class ChangeLogAdmin(admin.ModelAdmin):
  ordering = ['-id']
  pass

class ConstantAdmin(admin.ModelAdmin):
  pass

class AdminGroupAdmin(admin.ModelAdmin):
  pass

admin.site.register(App, AppAdmin)
admin.site.register(AppApply, AppApplyAdmin)
admin.site.register(AppReview, AppReviewAdmin)
admin.site.register(ChangeLog, ChangeLogAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Constant, ConstantAdmin)
admin.site.register(AdminGroup, AdminGroupAdmin)
