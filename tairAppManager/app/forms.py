# -*- coding: utf-8 -*-
from django import forms
from tairAppManager.cluster.models import Cluster,Group
from tairAppManager.app.models import app_status

class ApplyForm(forms.Form):
  name = forms.CharField(label=u'应用名称')
  describe = forms.CharField(label=u'应用描述', widget=forms.Textarea)
  qps = forms.IntegerField(label=u'访问次数')
  entry_num = forms.FloatField(label=u'条目数')
  capacity = forms.IntegerField(label=u'预计容量 单位M')

  #cache_or_durable = forms.BooleanField(widget=RadioSelect(choices=((True,u"缓存"),(False,u"持久化")), renderer=InlineRadioFieldRenderer),required=True,label=u'是否使用缓存,') 
  #restful_api = forms.BooleanField(required=True,label=u'是否使用Restful接口')
  #trade_critical = forms.BooleanField(required=True,label=u'Tair故障是否影响交易')
  #used_tair_before = forms.BooleanField(required=True,label=u'是否已经使用Tair')
  #data_source = forms.BooleanField(required=True,label=u'后方是否有数据源')
  #complicate_datastruct = forms.BooleanField(required=True,label=u'是否需要使用set,list,map等数据结构')
  get_none_key = forms.BooleanField(required=False,label=u'是否大量访问不存在key')
  two_cluster = forms.BooleanField(required=False,label=u'是否需要部署双机房')
  cache_or_durable = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"缓存"),(0,u"持久化")),required=True,label=u'是否使用缓存,') 
  restful_api = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"是"),(0,u"否")),required=True,label=u'是否使用Restful接口')
  trade_critical = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"是"),(0,u"否")),required=True,label=u'Tair故障是否影响交易')
  used_tair_before = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"是"),(0,u"否")),required=True,label=u'是否已经使用Tair')
  data_source = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"有"),(0,u"无")),required=True,label=u'后方是否有数据源')
  complicate_datastruct = forms.TypedChoiceField(widget=forms.RadioSelect,coerce=lambda x: bool(int(x)), choices=((1,u"是"),(0,u"否")),required=True,label=u'是否需要使用set,list,map等数据结构')
   
  notes = forms.CharField(required=False,label=u'备注', widget=forms.Textarea)
  username = forms.CharField(label=u'应用负责人')
  email= forms.EmailField(required=False,label=u'邮件地址')

class ReviewForm(forms.Form):
  group = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(cluster__property='2'),label=u'应用名称')
  #group_name = forms.CharField(max_length = 30)
  namespace = forms.IntegerField(label=u'NameSpace')
  #version = forms.CharField(max_length = 30,label=u'客户端版本')
  quota = forms.IntegerField(label=u'配额容量', initial=-1)
  status = forms.ChoiceField(choices=app_status, initial='3',label=u'申请状态')

class sendForm(forms.Form):
  message = forms.CharField(label=u'邮件内容', widget=forms.Textarea)

