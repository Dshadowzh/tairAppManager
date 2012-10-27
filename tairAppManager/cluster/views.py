# -*- coding: utf-8 -*-

from tairAppManager.cluster.models import Cluster,Group
from tairAppManager.app.models import App, AppReview, AppApply
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponse,HttpResponseNotFound
import json

class HttpResponseConflict(HttpResponse):
  status_code = 409
    
def getAllCluster(request):
  if request.method == 'GET':
    dict={}
    group_list=[]
    group_data = []
    ctype = request.GET.get("type","")
    if ctype == "" or ctype == "all":
      group_list = Group.objects.all()
    elif ctype == "mdb":
      group_list = Group.objects.filter(cluster__storage="1")
    elif ctype == "rdb":
      group_list = Group.objects.filter(cluster__storage="2")
    elif ctype == "ldb":
      group_list = Group.objects.filter(cluster__storage="3")
    elif ctype == "daily":
      group_list = Group.objects.filter(cluster__property="1")
    elif ctype == "online":
      group_list = Group.objects.filter(cluster__property="2")
    for group in group_list:
      group_map = {
        'id' : group.id,
        'name' : u'%s/%s'%(group.cluster.cluster_name,group.name), 
        'cs' : group.get_cs(), 
        'ds' : group.get_ds(), 
        'ds_num' : group.cluster.ds_num, 
        'type' : u'%s/%s'%( group.cluster.get_distrib_display(), group.cluster.get_storage_display()) ,
        'app' : group.app_num, 
      }
      monitor_list = group.monitor_addr.split(" ")
      for (i, monitor_addr) in enumerate(monitor_list):
        group_map['monitor'+str(i)]=monitor_addr
      group_data.append(group_map)
    return render_to_response('clusters.html', {'groups':group_data, "ctype":ctype},context_instance=RequestContext(request))

def getUnusedNamespace(request, group_id):
  if request.method == 'GET':
    try:
      group_info = Group.objects.get(id=group_id)
      ns = group_info.get_unused_namespace() 
      if ns > 0:
        return HttpResponse(json.dumps({'namespace':ns}))
      return HttpResponse(json.dumps({'error':'Namespace Not Found'}))
    except:  
      return HttpResponse(json.dumps({'error':'Group Not Found'}))

def checkNamespace(request, group_id):
  if request.method == 'GET':
    try:
      namespace = request.GET.get("namespace")
      if ( int(namespace) > 1024) or (int(namespace) < 0) :
        return HttpResponse(json.dumps({'error':'namespace out of range'}))
      group_info = Group.objects.get(pk=group_id)
      exist = group_info.check_namespace(namespace)
      print namespace, exist
      return HttpResponse(json.dumps({'exist':exist}))
    except Exception, e:  
      print e 
      return HttpResponse(json.dumps({'error':'Group Not Found'}))

def getTest(request):
  if request.method == 'GET':
    return render_to_response('test.html', context_instance=RequestContext(request))

def getApps(request):
  if request.method == 'GET':
    return render_to_response('test.html', context_instance=RequestContext(request))

def getManger(request, group_id):
  if request.method == 'GET':
    group_info = get_object_or_404(Group, id=group_id)
    return render_to_response('manage.html', {'groupname':group_info.name, 'monitor':group_info.monitor_addr }, 
                              context_instance=RequestContext(request))

def getNodes(request):
  if request.method == 'GET':
    return render_to_response('test.html', context_instance=RequestContext(request))

def getCluster(request,group_id):
  group_info = Group.objects.get(id=group_id)
  group_data = {}
  group['id']= group_info.id
  group['name']= group_info.name
  group['info']= group_info.id
  apps = AppReview.objects.filter(group=group_info)
  #group['id']= group_info.id
  return render_to_response('group.html', {'app':apps}, context_instance=RequestContext(request))
  
