# -*- coding: utf-8 -*-

from tairAppManager.cluster.models import Cluster
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context,Template
from django.http import HttpResponse,HttpResponseRedirect
import os
  
def messageHome(request):
  value=''
  for key in os.environ.keys(): 
    value+= ' '+key
  return HttpResponse("work in process %s "%(value))
