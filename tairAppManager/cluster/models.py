# -*- coding: utf-8 -*-

from django.db import models

cluster_type = (
  ('1', 'mdb '), 
  ('2', 'rdb '), 
  ('3', 'ldb '),  
  ('4', 'kdb '),
)

distrib_type = (
  ('1', u'单机房单集群'),
  ('2', u'双机房单集群单份'),
  ('3', u'双机房单集群双份'),
  ('4', u'双机房独立集群'),
  ('5', u'双机房主备集群'),
)

property_type = (
  ('1', u'日常'),
  ('2', u'线上'),
  ('3', u'预发'),
  ('4', u'已下线'),
)

class Cluster(models.Model):
  '''
    basic info of cluster
  '''
  # name of cluster
  cluster_name = models.CharField(max_length = 30)
  # the url of cluster info
  url = models.TextField(default = "")
  # storage type 
  storage = models.CharField(max_length = 1, choices = cluster_type)
  # version of tair client
  vers = models.CharField(max_length = 30)
  # detail version of tair 
  vers_detail = models.CharField(max_length = 30)
  # this cluster is the online, daily, or prerelease
  property = models.CharField(max_length = 1, choices = property_type)
  # summary of the app
  summary = models.TextField(default = "")
  # function of the app
  func = models.TextField(default = "")
  # the num of ds
  ds_num = models.IntegerField(default = 0)
  # the url in pe system where we can see the ds list
  ds_list = models.TextField(default = "")
  # invlid server list
  ivs_list = models.TextField(default = "")

  distrib = models.CharField(max_length = 1, choices = distrib_type)
  #
  master_1 = models.TextField(default = "")
  slave_1 = models.TextField(default = "")
  master_2 = models.TextField(default = "")
  slave_2 = models.TextField(default = "")
  diamond = models.TextField(default = "")

  # the cluster of daily
  #daily_enviro = models.IntegerField(default = -1)
  daily_enviro = models.ForeignKey("self", related_name="daily", blank=True, null=True)
  prerelease_enviro = models.ForeignKey("self", related_name="prerelease", blank=True, null=True)
  sandbox_enviro = models.ForeignKey("self", related_name="sandbox", blank=True, null=True)

  def __unicode__(self):
    return u'%d)%s'%(self.id,self.cluster_name)

  def get_cs(self):
    if self.distrib == '1' or self.distrib == '2' or self.distrib == '3':
      return u'\
      master cs: %s\n \
      slave cs: %s\n \
      '%(self.master_1 ,self.slave_1)
    elif self.distrib == '4' or self.distrib == '5':
      return u'\
      diamond: "%s"\n \
      master cs: %s\n \
      slave cs: %s\n \
      master cs2: %s\n \
      slave cs2: %s\n \
      '%(self.diamond, self.master_1, self.slave_1, self.master_2, self.slave_2)
    else :
      return u'\
      master cs: %s\n \
      slave cs: %s\n \
      '%(self.master_1 ,self.slave_1)

  def get_ds(self):
    return self.ds_list
  
  def get_diamond(self):
    if self.diamond and self.diamond.strip() != "none" and self.diamond.strip() != "":
      print self.diamond
      if len(self.diamond.split("&dataId=")) > 1:
        link = self.diamond
        configId = self.diamond.split("&dataId=")[1].split("&group=")[0]
        print configId
        return "Diamond configId:<a href=\"%s\">%s</a>"%(link, configId)
      else :
        return self.diamond
    else:
      return "\n%s"% self.get_cs() 

#  def get_daily_cs(self):
#    if self.daily_enviro==-1:
#      return u"daily 未配置"
#    else:
#      try:  
#        daily= Cluster.objects.get(pk=self.daily_enviro) 
#        return daily.get_cs()
#      except:
#        return u"未找到关联daily %d",self.cluster.daily_enviro

  def get_daily(self):
    if self.daily_enviro:
      return self.daily_enviro.get_diamond() 
    else :
      return u"  未关联"

  def get_prerelease(self):
    if self.prerelease_enviro:
      return self.prerelease_enviro.get_cs() 
    else:
      return u"  同线上集群"

  def get_sandbox(self):
    if self.sandbox_enviro:
      return self.sandbox_enviro.get_cs() 
    else:
      return u"  未关联"

  def display(self):
    return u'存储类型 :%s\n客户端版本 :%s\n日常环境配置 :\n%s\n生产环境配置: \n %s\n预发布环境配置: \n %s\n沙箱环境配置: \n %s\n ' \
      %(self.get_storage_display(), self.vers, self.get_daily(), self.get_cs(), self.get_prerelease(), self.get_sandbox())

  def mail(self):
    return u' 存储类型 :%s\n 客户端版本 :%s\n 日常环境配置 :%s\n 生产环境配置: \n %s\n ' \
      %(self.get_storage_display(), self.vers, self.get_daily(), self.get_diamond())

class Group(models.Model):
  '''
    basic info of group
  '''
  # name of group
  name = models.CharField(max_length = 30);
  # the num of app used
  app_num = models.IntegerField(default = 0)
  # max namesapce till now
  max_namespace = models.IntegerField(default = 100)
  # the mointor address of the cluster
  monitor_addr = models.TextField()
  
  # cluster of the group
  cluster = models.ForeignKey(Cluster)

  #----- backup field
  # the type of storage engine
  #storage_type = models.CharField(max_length = 3, choices = cluster_type)

  def __unicode__(self):
    return u'%d) %s/%s'%(self.id, self.cluster.cluster_name , self.name)

  def get_cs(self):
    return self.cluster.get_cs()

  def get_ds(self):
    return self.cluster.get_ds()


  def get_client_version(self):
    return self.cluster.version_of_client 

  def incr_app_num(self):
    self.app_num+=1
    self.save()

  #更新最大的namespace
  def update_max_namespace(self, new_namespace):
    if new_namespace > self.max_namespace :
      self.max_namespace = new_namespace
      self.save()
      return 1
    return -1

  def get_unused_namespace(self):
#TODO: find availble
    return self.max_namespace+1

  def check_namespace(self, namespace):
    for app in self.appreview_set.all():
      if str(app.namespace) == namespace: 
        return True
    return False 
    #return (len(App.objects.filter(namespace=namespace, group=self.id))>0) and Ture or False 

  def display(self):
    return u'%s\n监控统计信息查看:\n%s\n' \
      %(self.cluster.mail(), self.monitor_addr)
