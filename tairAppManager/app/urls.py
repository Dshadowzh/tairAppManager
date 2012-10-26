# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from tairAppManager.app.views import *
from tairAppManager.app.helper import *

urlpatterns = patterns('tairAppManager.app', 
   (r'^$','views.getAllApp'),
   (r'^json$','views.getAllAppJson'),
   (r'^apply$','views.newApply'),
   (r'^thanks$','views.thanks'),
   (r'^(?P<apply_id>\d+)/$','views.getApply'),
   (r'^(?P<app_id>\d+)/review/$','views.newReview'),
   (r'^(?P<app_id>\d+)/rereview/$','views.reReview'),
   (r'^(?P<app_id>\d+)/decline$','views.declineReview'),
   (r'^(?P<app_id>\d+)/mail/$','views.sendMail'),
   (r'^(?P<app_id>\d+)/setimportant/$','views.modifyImportant'),
   (r'^(?P<app_id>\d+)/edit/?$','views.editApp'),
   (r'^(?P<apply_id>\d+)/editapply$','views.editApply'),
   (r'^savecb','helper.saveClipBoard'),
   #(r'^(?P<apply_id>\d+)/review/$','views.reviewApply'),
)
