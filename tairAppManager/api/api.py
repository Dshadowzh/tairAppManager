# -*- coding: utf-8 -*-

from tairAppManager.cluster.models import Group, Cluster
from tairAppManager.app.models import App, AppReview, AppApply
from tairAppManager.tair.taircmd import *

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json

def getgroup(data):
  cs_1 = data.get("cs1", None)
  cs_2 = data.get("cs2", None)
  group = data.get("group", None)
  cluster= data.get("cluster", None)
  dbtype = data.get("dbtype", "mdb")
  if (cs_1 or cs_2) and group :
    pass 
  elif cluster and group :
    return findGroup(cluster, group)
  else:
    return findGroupAuto(dbtype)

def findGroupAuto(ctype):
  if ctype == "mdb":
    return findGroup("aliyun_ace_test", "group_1")
  if ctype == "rdb":
    pass
  if ctype == "ldb":
    pass
  else:
    pass
  return None 

def findGroup(clustername, groupname):
  c = Cluster.objects.filter(cluster_name=clustername)
  if (c.count() == 0):
    return None
  glist =  Group.objects.filter(cluster=c) 
  for g in glist:
    if g.name == groupname:
      return g
  return None

@csrf_exempt
def area(request, area_key):
  if request.method == 'POST':
    ctype = request.POST.get("type", "")
    quota = request.POST.get("quota", -1)
    print "post ", area_key, ctype, quota
    try:
      q = int(quota)
    except :
      return HttpResponseBadRequest("quota invalid")
    #if q <= 0:
    #  return HttpResponseBadRequest("quota invalid")
    if ctype == "alloc0" or ctype == "alloc1": 
      app = App.objects.filter(name=area_key)
      if app.count() != 0:
        return HttpResponseConflict("app key existed!")
      apply = AppApply(name=area_key,describe="system auto",qps=0,capacity=q,notes="",
        cache_or_durable=True,restful_api=False,trade_critical=False,
        data_source=False,complicate_datastruct=False,entry_num=0,
        get_none_key=False, two_cluster=True, used_tair_before=False,
        create_by_username="system",email="app.tair@taobao.com")
      apply.save()
      app = App(name=area_key, status='1', important='3', apply=apply)
      app.save() 
      g = findGroupAuto("mdb")
      if g == None:
        return HttpResponseNotFound("suitable group not found!")
      (ret, res) = allocNamespace(area_key ,q, g, app, ctype)
      if ret == TAIR_SUCCESS:
        return HttpResponse(json.dumps(res))
      else:
      	print "alloc ns error"
        return HttpResponse({'error':res})
  
    elif ctype == "modify":
      app = App.objects.filter(name=area_key)
      if (app.count() == 0):
        return HttpResponseNotFound("area key not existed!")
      if not app[0].review:
        return HttpResponseNotFound("area key not reviewed!")
      group = app[0].review.group
      ret = setQuota(area_key, quota, group, app[0])
      if ret == TAIR_SUCCESS: 
        app.review.quota = quota
        app.review.save()
        return HttpResponse(json.dumps({'error':'OK'}))
      else :
        return HttpResponse(json.dumps({'error':'error'}))

    else :
      return HttpResponseBadRequest("ctype invalid")


  if request.method == 'GET':
    ctype = request.GET.get("type", None)
    #quota = request.POST.get("quota", -1)
    #cs_1 = request.POST.get("cs1", None)
    #cs_2 = request.POST.get("cs2", None)
    #group = request.POST.get("group", None)
    #cluster_id = request.POST.get("cluster", -1)
    print "hello"
    if ctype == 'cluster':
      print  "hello2"
      g = findGroupAuto("mdb")
      if g == None:
        return HttpResponseNotFound("suitable group not found!")
      app = App.objects.filter(name=area_key)
      if (app.count() == 0):
        return HttpResponseNotFound("area key not existed!")
      area_num = app[0].review.namespace
      quota = app[0].review.quota
      (ret, res)= getClusterInfo(g, area_num, quota)
      if ret == TAIR_SUCCESS: 
        return HttpResponse(json.dumps(res))
      else :
        return HttpResponseNotFound("area cluster info not found!")
    if ctype == 'stat':
      print "hello3"
      app = App.objects.filter(name=area_key)
      if (app.count() == 0):
        return HttpResponseNotFound("area key not existed!")
      if not app[0].review:
        return HttpResponseNotFound("area key not reviewed!")
      group = app[0].review.group
      (ret, res) = getAreaStat(key, group, app)
      if ret == TAIR_SUCCESS: 
        return HttpResponse(json.dumps(res))
      else :
        return HttpResponseNotFound("area key not existed!")
    return HttpResponse("please indicate type")
    

  if request.method == 'DELETE':
    app = App.objects.filter(name=area_key)
    if (app.count() == 0):
      return HttpResponseNotFound("area key not existed!")
    if not app[0].review:
      return HttpResponseNotFound("area key not reviewed!")
    ret = setQuota(area_key, quota, group, app)
    if ret == TAIR_SUCCESS: 
      app[0].review.delete()
      app[0].apply.delete()
      app[0].delete()
      return HttpResponse(json.dumps(res))
    else :
      return HttpResponseNotFound("area key delete failed!")
  
@csrf_exempt
def cluster(request, cluster_id):
  pass

@csrf_exempt
def node(request, node_id):
  pass

def rDelQuota(request):
  if request.method == 'POST':
    key = request.POST.get("key", -1)
    app = App.objects.filter(name=key)
    if (app.count() == 0):
      return HttpResponseNotFound("area key not existed!")
    #area = str(app[0].review.namespace)
    ret = setQuota(area, quota, group, app)
    if ret == TAIR_SUCCESS: 
      return HttpResponse(json.dumps({'error':'OK'}))
    else :
      return HttpResponse(json.dumps({'error':'error'}))

def rSetQuota(request):
  if request.method == 'POST':
    key = request.POST.get("key", -1)
    app = App.objects.filter(name=key)
    if (app.count() == 0):
      return HttpResponseNotFound("area key not existed!")
    #area = str(app[0].review.namespace)
    quota = request.POST.get("quota", 0)
    try:
      q = int(quota)
    except :
      return HttpResponseBadRequest("quota invalid")
    g = findGroupAuto("mdb")
    ret = setQuota(key, quota, group, app)
    if ret == TAIR_SUCCESS: 
      return HttpResponse(json.dumps({'error':'OK'}))
    else :
      return HttpResponse(json.dumps({'error':'error'}))

def rAllocNamespace(request):
  if request.method == 'POST':
    key = request.POST.get("key", -1)
    app = App.objects.filter(name=key)
    if (app.count() != 0):
      return HttpResponseConflict("app key existed!")
    quota = request.POST.get("quota", 0)
    try:
      q = int(quota)
    except:
      return HttpResponseBadRequest("quota invalid")
    #mastercs = request.POST.get("mastercs", "")
    #slavecs = request.POST.get("slavecs", "")
    clustername = request.POST.get("clustername", "")
    groupname = request.POST.get("groupname", "")

    try:
      tc = tairclient(mastercs, slavecs, groupname)
      new_area = tc.alloc_namespace(key, q)
      return HttpResponse(json.dumps({'areanum':new_area}))
    except e:
      print e
      return HttpResponse(json.dumps({'error':'error'}))
  return HttpResponse(json.dumps({'error':'OK'}))

