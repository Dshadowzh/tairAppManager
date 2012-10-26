# -*- coding: utf-8 -*-
from django.db import models
from tairAppManager.cluster.models import Cluster,Group
from django.contrib.auth.models import User 

class AppApply(models.Model):

  name = models.TextField()
  describe = models.TextField()
  # 访问次数 
  qps = models.FloatField()
  # 条目数
  entry_num = models.FloatField()
  # 预计容量 单位M
  capacity = models.IntegerField()

  # 缓存ture 持久化false
  cache_or_durable = models.BooleanField() 
  # 是否需要使用restful接口
  restful_api = models.BooleanField()
  # Tair故障是否影响交易
  trade_critical = models.BooleanField()
  # 是否已经使用Tair
  used_tair_before = models.BooleanField()
  # 后方是否有数据源
  data_source = models.BooleanField()
  # 是否需要使用set,list,map等数据结构
  complicate_datastruct = models.BooleanField()
  # 是否大量访问不存在key
  get_none_key = models.BooleanField()
  # 是否需要双机房部署
  two_cluster = models.BooleanField()
  # 备注
  notes = models.TextField()

  create_by_username = models.CharField(default="", max_length=30)
  create_by= models.ForeignKey(User,related_name="apply_create_by_user", blank=True, null=True)
  create_by_uid = models.IntegerField(default = -1)
  create_at= models.DateTimeField(auto_now_add=True)

  modify_by_username = models.CharField(default="", max_length=30)
  modify_by= models.ForeignKey(User,related_name="apply_modify_by_user", blank=True, null=True)
  modify_by_uid = models.IntegerField(default = -1)
  modify_at= models.DateTimeField(auto_now=True)

  #----- backup field
  #备用email 
  email= models.EmailField(default="")

  def modify_apply(self,name,describe,qps,capacity,cache_or_durable,restful_api,trade_critical,used_tair_before,data_source,complicate_datastruct,create_by_username,email, modify_by_username,modify_at, entry_num, notes):
    print self.cache_or_durable,cache_or_durable 
    self.name = name 
    self.describe = describe
    self.qps = qps
    self.capacity = capacity
    self.cache_or_durable = (cache_or_durable == "True")
    self.restful_api = (restful_api == "True")
    self.trade_critical = (trade_critical == "True")
    self.used_tair_before = (used_tair_before == "True")
    self.data_source = (data_source == "True")
    self.complicate_datastruct = (complicate_datastruct == "True")
    self.create_by_username = create_by_username
    self.modify_by_username = modify_by_username
    self.notes = notes
    self.entry_num = entry_num 
    self.modify_at = modify_at
    print self.cache_or_durable,cache_or_durable 
    self.save() 

  def modify_apply_f(self, form):
    pass

  def __unicode__(self):
    return u'%d)%s'%(self.id,self.name)

class AppReview(models.Model):
  group = models.ForeignKey(Group, null=True)
  group_name = models.CharField(max_length = 30)
  namespace = models.IntegerField()
  version = models.CharField(max_length = 30)
  # 分配配额容量 单位M
  quota = models.IntegerField(default=0)

  review_by= models.ForeignKey(User,related_name="review_by_user",blank=True, null=True)
  review_by_username = models.CharField(default="", max_length=30)
  review_at= models.DateTimeField(auto_now=True)
  
  # 旧系统中导入的应用 Ture 表示旧的，False 表示新的
  old_type = models.BooleanField()
  #mail = models.ForeignKey("ReviewMail",relate_Nmae="review_mail",blank=True, null=True)
  mail_id = models.IntegerField(default=-1)

  # 备注
  notes = models.TextField()
  #def __init__(gourp, group_name, auto_alloc, namespace, version, quota, review_by, review_by_username, review_at):
  #  self.group = group
  #  self.group_name = group_name
  #  #if auto_alloc == True:
  #  #  area = 
  
  def set_quota(quota):    
    self.quota = quota
    self.save()

  def change_namespace(namespace):    
    self.namespace = namespace
    self.save()

  def __unicode__(self):
    if self.group:
      return u'%d)%s/%s:%d'%(self.id, self.group.cluster.cluster_name, self.group_name, self.namespace)
    else:
      return u'not review'

  def display(self):
    return u'%s namespace: %s\n 配额容量: %sM\n'\
      %(self.group.display(), self.namespace, self.quota)

app_status = (('1', u'待审批'), ('2', u'已审批未部署'), ('3', u'已部署'),  ('4', u'拒绝'),)
important_level = (('0', u'待补充'), ('1', u'核心'), ('2', u'非核心'), ('3', u"系统自动"))

class App(models.Model):
  name = models.TextField()
  status = models.CharField(max_length=1,choices = app_status)
  
  important = models.CharField(max_length=1,choices = important_level, default='0')

  apply = models.ForeignKey("AppApply")  

  review = models.ForeignKey("AppReview",blank=True,null=True)
  
  #def modify_app():
  #  pass

  def change_status(self, status):
    self.status=status
    self.save()

  def add_review(self, review):
    self.review=review
    self.save()

  def __unicode__(self):
    return u'%d)%s'%(self.id,self.name)

  def set_important_level(self, i):
    self.important=i
    self.save()
    return 

  #获取dataTable插件需要格式的JSON数据
#  @staticmethod 
#  def get_dataTable_json():
#    dict={}
#    app_list = App.objects.all() 
#    dict["iTotalRecords"] = app_list.count()
#    dict["iTotalDisplayRecords"] = dict["iTotalRecords"] 
#    app_data = []
#    for app in app_list:
#      if app.review != -1:
#        review = AppReview.objects.get(pk=app.review)
#        app_data.append([app.name, app.apply.describe, app.status, app.apply.create_by.username, 
#            review.group.__unicode__(), review.namespace, 'edit',])
#      else:
#        app_data.append([app.name, app.apply.qps, "None",' ' ,'' ,'',''])
#      #app_data.append([a.name, a.apply.create_by.name, a.apply.create_at, review.cluster.name])
#    dict["aaData"]=app_data
#    return dict

class ReviewMail(models.Model):
  mail_content = models.TextField()
  modify_by_username = models.CharField(default="", max_length=30)
  #modify_by = models.ForeignKey(User,related_name="mail_modify_by_user", null=True, blank=True)
  modify_by = models.IntegerField(default=-1)
  modify_at = models.DateTimeField(auto_now=True)

class ChangeLog(models.Model):
  change = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return u'%s'%(self.change)

class Feedback(models.Model):
  commet = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)
  username = models.CharField(default="", max_length=30)
  def __unicode__(self):
    return u'%d)%s'%(self.id, username)

class Constant(models.Model):
  key = models.CharField(max_length=30, primary_key=True)
  value = models.TextField()
  def __unicode__(self):
    return u'%s'%(self.key)


class AdminGroup(models.Model):
  username = models.CharField(default="", max_length=30)
  clipboard = models.TextField(null=True, default="")
  def __unicode__(self):
    return u'%s'%(self.username)
	
