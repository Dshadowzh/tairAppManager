# -*- coding: utf-8 -*-

from tairAppManager.cluster.models import Group, Cluster
from tairAppManager.app.models import App, AppReview, AppApply
#from pytair.pytair import tairclient
from tairAppManager.tair.tairclient import tairclient

TAIR_SUCCESS, TAIR_FAILURE = 0, -1

def allocNamespace(key, quota, group, app, ctype):
  print group.cluster.master_1, group.cluster.slave_1, group.name, group.cluster.diamond, key, quota
  #print "client start"
  tc = tairclient(group.cluster.master_1, group.cluster.slave_1, group.name)
  #tc = tairclient('10.249.199.174:5198', '10.249.199.184:5198', 'group_1')
  #print "client ok"
  new_area = tc.alloc_namespace(key, quota)
  try:
    # new appreview
    review = AppReview(group=group, 
        namespace=new_area, version='', quota=quota ,
        review_by_username="Sys", old_type=False)
    review.save()
    app.add_review(review)
    app.change_status('3')
    #print "ok", ctype
    #print group.name
    #print group.cluster.master_1
    #print group.cluster.slave_1
    #print group.cluster.master_2
    #print group.cluster.slave_2
    gdict=[]
    if ctype == "alloc0":
      return (TAIR_SUCCESS, {'areanum':new_area, 'diamond':group.cluster.diamond})
    if ctype == "alloc1":
      distrib = group.cluster.distrib
      if distrib == '1'  or distrib == '2' or distrib == '3':
        #print {'areanum':new_area, 'address':{'group':group.name,'master':group.cluster.master_1,'slave':group.cluster.slave_1}}
        gdict.append({'areanum':new_area,
               'address':{'group':group.name,'master':group.cluster.master_1,'slave':group.cluster.slave_1}})
      if distrib == '4'  or distrib == '5':
        #print {'areanum':new_area,'group':group.name,'master':group.cluster.master_2,'slave':group.cluster.slave_2}
        gdict.append({'areanum':new_area,
               'address':{'group':group.name,'master':group.cluster.master_2,'slave':group.cluster.slave_2}})
      return (TAIR_SUCCESS, {'clusters':gdict})
  except ValueError as e:
    return (TAIR_FAILURE, e)

def getClusterInfo(group, area, quota):
  try:
    gdict=[]
    distrib = group.cluster.distrib
    if distrib == '1'  or distrib == '2' or distrib == '3':
      gdict.append({'areanum':area, 'quota':quota,
             'address':{'group':group.name,'master':group.cluster.master_1,'slave':group.cluster.slave_1}})
    if distrib == '4'  or distrib == '5':
      gdict.append({'areanum':area, 'quota':quota,
             'address':{'group':group.name,'master':group.cluster.master_2,'slave':group.cluster.slave_2}})
    return (TAIR_SUCCESS, {'clusters':gdict})
  except ValueError as e:
    return (TAIR_FAILURE, e)

def setQuota(area, quota, group, app):
  print "xx"
  try:
    print "0"
    tc = tairclient(group.cluster.master_1, group.cluster.slave_1, group.name)
    print "0"
    tc.modify_quota(area, quota)
    print "1"
    review = app.review
    print "2"
    review.quota = quota
    review.save()
    print "3"
    return TAIR_SUCCESS
  except:
    return TAIR_FAILURE

def deleteQuota(area, group, app):
  try:
    tc = tairclient(group.cluster.master_1, group.cluster.slave_1, group.name)
    tc.modify_quota(area, 0)
    review = app.review
    review.set_quota(0)
    return TAIR_SUCCESS
  except:
    return TAIR_FAILURE

def getAreaStat(area, group, app):
  try:
    tc = tairclient(group.cluster.master_1, group.cluster.slave_1, group.name)
    stat = tc.get_stat(area)
    print stat
    return (TAIR_SUCCESS, stat)
  except:
    return (TAIR_FAILURE, "error")
