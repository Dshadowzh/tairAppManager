# -*- coding: utf-8 -*-

from django.contrib.auth.models import User 
from tairAppManager.app.models import App, AppApply, AppReview, ReviewMail, Constant, AdminGroup
from tairAppManager.cluster.models import Cluster,Group
from tairAppManager.ssouser.models import *
from tairAppManager.app.forms import *
from tairAppManager.utils.format import cutline, removeComment
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext,Template
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import json, re, sys, time, smtplib

def tair_authenticatied():
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)

def newApply(request):
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  applicant = sso_user_get_username(request)
  uid = sso_user_get_empid(request)
  applicant_mail = sso_user_get_email(request)
  if request.method == 'POST':
    form = ApplyForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      applicant = data["username"]
      applicant_mail = data["email"]
      if sso_user_is_authenticated(request) :
        #apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=u"#department:%s company:%s\n%s"%(sso_user_get_dep(request),sso_user_get_corp(request) ,data["notes"]),
        apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=data["notes"],
          cache_or_durable=data['cache_or_durable'],restful_api=data['restful_api'],trade_critical=data['trade_critical'],
          data_source=data['data_source'],complicate_datastruct=data['complicate_datastruct'],entry_num=data["entry_num"],
          get_none_key=data['get_none_key'], two_cluster=data['two_cluster'], used_tair_before=data['used_tair_before'],
          create_by_username=applicant, modify_by_username=applicant, email=applicant_mail)
      elif request.user.is_authenticated():
        #apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=u"#部门:%s 公司:%s\n%s"%(sso_user_get_dep(request),sso_user_get_corp(request) ,data["notes"]),
        apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=data["notes"],
          cache_or_durable=data['cache_or_durable'],restful_api=data['restful_api'],trade_critical=data['trade_critical'],
          data_source=data['data_source'],complicate_datastruct=data['complicate_datastruct'],entry_num=data["entry_num"],
          get_none_key=data['get_none_key'], two_cluster=data['two_cluster'], used_tair_before=data['used_tair_before'],
          create_by=request.user, modify_by=request.user, email=applicant_mail)
      else:
        #apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=u"#部门:%s 公司:%s\n%s"%(sso_user_get_dep(request),sso_user_get_corp(request) ,data["notes"]),
        apply = AppApply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=data["notes"],
          cache_or_durable=data['cache_or_durable'],restful_api=data['restful_api'],trade_critical=data['trade_critical'],
          data_source=data['data_source'],complicate_datastruct=data['complicate_datastruct'],entry_num=data["entry_num"],
          get_none_key=data['get_none_key'], two_cluster=data['two_cluster'], used_tair_before=data['used_tair_before'],
          email=applicant_mail)
      apply.save()
      app = App(name=data['name'], status='1', apply=apply)
      app.save() 
      if data['email']:
        return render_to_response('thanks.html', {'email': data['email']},context_instance=RequestContext(request))
      else:
        return HttpResponseRedirect('/app/thanks')
  else:
      #desc_tip=u"#业务场景 KeyValue分别是什么，keyValue的大小\n\n#访问特点 读写比例 访问时间（高峰时间）\n\n#数据量大小，每天数据增量\n\n#对访问响应时间有什么要求\n "
      try:
        desc_tip = Constant.objects.get(key="t_describe_apply").value
      except Constant.DoesNotExist:
        desc_tip = None
      form = ApplyForm(initial={'describe':desc_tip})
  tip={}
  tip["username"]=applicant
  tip["email"]=applicant_mail
  return render_to_response('newapply.html', {'form': form, 'tips':tip},context_instance=RequestContext(request))

def getAppData(app):
  data=[]
  if app.review:
    #review = AppReview.objects.get(pk=app.review)
    review = app.review
    if review.group: 
      cluster= review.group.cluster.cluster_name 
    else:
      cluster=""
    data={
      'id' : app.id,
      'applyid' : app.apply.id,
      'name' : app.name, 
      'describe' : app.apply.describe, 
      'status' : app.get_status_display(), 
      'applicant' : (app.apply.create_by) and app.apply.create_by.username or app.apply.create_by_username, 
      'cluster' : cluster,
      'namespace' : review.namespace, 
      'important' : app.get_important_display(),
    }
  else:
    data={
      'id' : app.id,
      'applyid' : app.apply.id,
      'name' : app.name, 
      'describe' : app.apply.describe, 
      'status' : app.get_status_display(), 
      'applicant' : (app.apply.create_by) and app.apply.create_by.username or app.apply.create_by_username, 
    }
  return data

#@cache_page(60 * 60 * 24)
def getAllApp(request):
  if request.method == 'GET':
    #app_list = App.objects.filter(important="0").order_by("-id")
    app_list = []
    ctype = request.GET.get("type","")
    page= render_to_response('home.html', {"ctype":ctype,'apply':True, 'apps':app_list},context_instance=RequestContext(request))
    #if ctype == "" or ctype == "all":
    #  page= render_to_response('home.html', {'apply':True, 'apps':app_list},context_instance=RequestContext(request))
    #elif ctype == "todo" :
    #  page= render_to_response('home.html', {"todo":ctype,'apply':True, 'apps':app_list},context_instance=RequestContext(request))
    #else:
    #  return HttpResponse("ok") 
    return page

def getAllAppJson(request):
  if request.method == 'GET':
    #data={"iTotalRecords":"4" ,'aaData':[[0,"22s",1,],[1,"22s",1,],[2,"3s",4,],[9,"4a",5,]]}
    ctype = request.GET.get("type","")
    if ctype == "" or ctype == "all":
      app_list = App.objects.filter(important="0")
    elif ctype == "todo":
      app_list = App.objects.filter(important="0", status="1")
    elif ctype == "done":
      app_list = App.objects.filter(status="3", important="0")
    else:
      return HttpResponse(json.dumps([]))
    #print len(app_list),ctype
    #data = get_dataTable_json(request, App.objects.filter(important="0"))
    data = get_dataTable_json(request, app_list)
    return HttpResponse(json.dumps(data))
  return HttpResponse(json.dumps([]))

def get_dataTable_json(request, querySet, jsonTemplatePath = None, *args):
  columns = ["id", "name", "desc", "status", "applicant", "cluster", "namespace", "op"]
  sColumns = ",".join(map(str,columns))
  asortingCols = []
  iStart = int(request.GET.get("iDisplayStart")) 
  iLength = int(request.GET.get("iDisplayLength")) 
  iEnd = iStart + iLength
  iSearch = request.GET.get("sSearch").encode('utf-8') 
  iSortingCols =  int(request.GET.get('iSortingCols',0))
  iecho = request.GET.get("sEcho")
  cols = int(request.GET.get('iColumns',0)) # Get the number of columns
  
  # 排序 
  if iSortingCols:
    for sortedColIndex in range(0, iSortingCols):
      sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
      if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  # make sure the column is sortable first
        sortedColName = columns[sortedColID]
        sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
        if sortingDirection == 'desc':
          sortedColName = '-'+sortedColName
        asortingCols.append(sortedColName)
    #print asortingCols
    querySet = querySet.order_by(*asortingCols)

  # 确定可以搜索的列
  searchableColumns = []
  for col in range(0,cols):
    if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columns[col])

  # 右上角的全文搜索 
  if iSearch != '':
    outputQ = None
    terms = iSearch.split()
    for term in terms:
      output1 = None
      kwargz = {"name__icontains" : term}
      output1 = output1 | Q(**kwargz) if output1 else Q(**kwargz)   
      kwargz = {"review__namespace__icontains" : term}
      output1 = output1 | Q(**kwargz) if output1 else Q(**kwargz)   
      kwargz = {"review__group__cluster__cluster_name__icontains" : term}
      output1 = output1 | Q(**kwargz) if output1 else Q(**kwargz)   
      kwargz = {"apply__create_by_username__icontains" : term}
      output1 = output1 | Q(**kwargz) if output1 else Q(**kwargz)   
      kwargz = {"apply__describe__icontains" : term}
      output1 = output1 | Q(**kwargz) if output1 else Q(**kwargz)   

      outputQ = outputQ & output1 if outputQ else output1
    querySet = querySet.filter(outputQ)

  # 单列搜索
  outputQ = None
  for col in range(0,cols):
    if request.GET.get('sSearch_{0}'.format(col), False) > '' and request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
      kwargz = {columns[col]+"__icontains" : request.GET['sSearch_{0}'.format(col)]}
      outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
  if outputQ: querySet = querySet.filter(outputQ)

  iTotalRecords = iTotalDisplayRecords = querySet.count() #count how many records match the final criteria
  querySet = querySet[iStart:iEnd] #get the slice
    
  if jsonTemplatePath:
    jstonString = render_to_string(jsonTemplatePath, locals()) #prepare the JSON with the response, consider using : from django.template.defaultfilters import escapejs
    return jsonString 
  else:
    aaData = []
    a = querySet.values() 
    for app in a:
      appo = App.objects.get(pk = app["id"])
      #apply = AppApply.objects.get(pk=int(app["apply_id"]))
      data = [
        app["id"],
        u"<a href=\"/app/%d/edit\">%s</a>"%(app["id"],cutline(app["name"],20)),
        cutline(removeComment(appo.apply.describe),35),
        appo.get_status_display(),
        appo.apply.create_by_username,
      ]
      try:
        if appo.review:
          data.append(appo.review.group.cluster.cluster_name)
          data.append(appo.review.namespace)
          #data.append(u"<a href=\"/app/%d/edit\">修&nbsp改</a>"%(app["id"]))
          data.append("")
        elif appo.status =='4':
          data.append("")
          data.append("")
          data.append("")
        else:
          data.append("")
          data.append("")
          data.append(u"<a href=\"/app/%d/review\">审&nbsp批</a>"%(app["id"]))
      except:
        data.append("")
        data.append("")
        data.append(u"<a href=\"/app/%d/review\">审&nbsp批</a>"%(app["id"]))
      aaData.append(data)
    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({'sEcho': iecho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    #print response_dict
    return response_dict

def getApply(request,apply_id):
  app_info = get_object_or_404(App, pk=apply_id)
  return render_to_response('apply.html', {'app': app_info},context_instance=RequestContext(request))

def eidtApply(request,apply_id):
  pass

def thanks(request):
  return render_to_response('thanks.html',context_instance=RequestContext(request))

@csrf_exempt
def declineReview(request, app_id):
  app = App.objects.get(pk=app_id)
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    decline = request.POST.get("decline","")
    if decline == "true":
      app.change_status("4")
  return HttpResponse(json.dumps([]))
      
def newReview(request, app_id):
  #未登陆
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  #如果不在admin组中,不能使用审批页面
  if len(AdminGroup.objects.filter(username=sso_user_get_username(request))) != 1 and not request.user.is_authenticated():
    error = u"对不起, %s 您没有审批权限, 需要开通请联系Tair答疑" % (sso_user_get_username(request))
    return render_to_response('alert.html',{"text":error},context_instance=RequestContext(request))
  #print app_id
  app = App.objects.get(pk=app_id)
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    decline = request.POST.get("decline","")
    if decline == True:
      app.change_status("4")
      return HttpResponse("ok")
    elif form.is_valid():
      data = form.cleaned_data
      #print data['group']
      g = Group.objects.get(pk=data['group']) 
      review = AppReview(group=g, 
          namespace=data['namespace'], version='', quota=data['quota'], 
          review_by_username=sso_user_get_username(request), old_type=False)
      review.save()
      app.add_review(review)
      app.change_status(data['status'])
      #if data['mail']:
      #  return render_to_response('thanks.html', {'mail': data['mail']},context_instance=RequestContext(request))
      #else:
      #  return HttpResponseRedirect('/app/thanks')

      #更新group信息
      g.incr_app_num()
      g.update_max_namespace(data['namespace'])
      return HttpResponseRedirect('/app/%s/mail'%(app_id))
    #print >> sys.stderr, form
  else:
      form = ReviewForm()
  return render_to_response('review.html', {'form': form, 'apply':app.apply},context_instance=RequestContext(request))

@csrf_exempt
def reReview(request, app_id):
  #未登陆
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponse(json.dumps({"errror":"no auth"}))
  #如果不在admin组中,不能使用审批页面
  if len(AdminGroup.objects.filter(username=sso_user_get_username(request))) != 1 and not request.user.is_authenticated():
    error = u'对不起, %s 您没有审批权限, 需要开通请联系Tair答疑' % (sso_user_get_username(request))
    return HttpResponse(json.dumps({"errror":"no permittion"}))
  #print "remove review, ", app_id
  try:
    app = App.objects.get(pk=app_id)
  except App.DoesNotExist:
    return HttpResponse(json.dumps({"errror":"no such appid"}))
  if request.method == 'POST':
    old_review = app.review
    if old_review:
      app.review = None
      app.status = '1'
      app.save()
      old_review.delete()
      return HttpResponse(json.dumps("ok"))
    else:
      return HttpResponse(json.dumps("ok"))
  

def sendMail(request, app_id):
  #未登陆
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  #如果不在admin组中,不能使用审批页面
  admin = AdminGroup.objects.filter(username=sso_user_get_username(request))
  if len(admin) != 1 and not request.user.is_authenticated() :
    error = u'对不起, %s 您没有审批权限, 需要开通请联系Tair答疑'%sso_user_get_username(request)
    return render_to_response('alert.html',{"text":error},context_instance=RequestContext(request))
  app_info = get_object_or_404(App, pk=app_id)
  #TODO:add mail choice
  applicant = app_info.apply.create_by_username
  mail_address = app_info.apply.email
  if request.method == 'POST':
    form = sendForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      title = u"Tair namespace申请反馈"
      #print title
      message = data["message"]
      #print message
      mail = ReviewMail(mail_content=message, modify_by_username=sso_user_get_username(request))
      mail.save()
      app_info.review.mail_id=mail.id
      app_info.review.save()
      msg = MIMEMultipart("alternative")
      msg["Subject"] = Header(title, 'utf-8')
      msg["From"] = settings.EMAIL_HOST_USER
      msg["To"] = mail_address
      msg["Content-type"] = "text/html;charset=utf-8"
      msg.attach(MIMEText(message.encode('utf8'), 'html', 'utf-8'))
      server = smtplib.SMTP(settings.EMAIL_HOST)
      try:
        server.sendmail(settings.EMAIL_HOST_USER, [mail_address], msg.as_string())
      except:
        HttpResponse(u"mail send failed!! address:%s"%mail_address)
      #send_mail(title, message, settings.EMAIL_HOST_USER,
      #    [mail_address], fail_silently=False)
      return HttpResponseRedirect('/app/')
  else:
      form = sendForm()
  review_info=app_info.review
  name = sso_user_get_username(request)
#  print review_info.group
#  print review_info.display()
#  base_mail= review_info.display()
  base_mail=u"namespace:%d<br>\n内存配额:%sM<br>\n客户端版本:%s<br>\n日常环境配置:%s<br>\n预发和生产环境配置：%s<br>\n统计信>息查询:%s<br>\n 请阅读<a href=\"http://baike.corp.taobao.com/index.php/QuickStartWithMcClient\">mc-client使用方法</a>\n "% (
             review_info.namespace, review_info.quota, review_info.group.cluster.vers,
             review_info.group.cluster.daily_enviro.get_diamond() if review_info.group.cluster.daily_enviro else "" ,
             review_info.group.cluster.get_diamond(),
             review_info.group.monitor_addr,)
  if review_info.group.cluster.distrib  == '4':
    base_mail += u"该集群部署方式为双机房独立集群，需要失效(删除)数据时，请使用invalid接口。 也就是DB有更新，需要调用invalid（会删除两边机房的tair key），参见<a href='http://baike.corp.taobao.com/index.php/Dds'>双机房独立集群容灾策略</a>"
  elif review_info.group.cluster.distrib  == '5':
    base_mail += u"该集群部署方式为双机房主备集群，参见<a href='http://baike.corp.taobao.com/index.php/Ddsm'>双机房主备集群容灾策略</a>"
  elif review_info.group.cluster.distrib  == '3':
    base_mail += u"该集群部署方式为双机房单集群双份，参见<a href='http://baike.corp.taobao.com/index.php/Dsd'>双机房单集群双份</a>"
  elif review_info.group.cluster.distrib  == '2':
    base_mail += u"该集群部署方式为双机房单集群单份，参见<a href='http://baike.corp.taobao.com/index.php/Dss'>双机房单集群单份</a>"
  #elif review_info.group.cluster.distrib  == '1':
  #  base_mail += u"该集群部署方式为单机房单集群，参见<a href='http://baike.corp.taobao.com/index.php/Dss'>双机房单集群单份</a>"
 
  clip = ""#admin[0].clipboard
  #print name, clip, admin[0].username
  return render_to_response('sendmail.html', {'reviewer':name, 'form': form, 'base_mail':base_mail, 'applicant':applicant, 'mail_address':mail_address, 'text':clip },
            context_instance=RequestContext(request))
  
def editApp(request, app_id):
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  app_info = get_object_or_404(App, pk=app_id)
  review = app_info.review
  apply = get_object_or_404(AppApply, pk=app_id)
  mail = None
  if review: 
    mail = (review.mail_id!=-1) and get_object_or_404(ReviewMail, pk=review.mail_id) or None
  return render_to_response('editapp.html', {'apply':apply, 'review':review, 'mail':mail}, context_instance=RequestContext(request))

def editApply(request, apply_id):
  apply = get_object_or_404(AppApply, pk=apply_id)
  #app_info = get_object_or_404(App, pk=apply_id)
  #apply = app_info.apply
  if request.method == 'POST':
    form = ApplyForm(request.POST)
    data = request.POST
    applicant = data["username"]
    applicant_mail = data["email"]
    if sso_user_is_authenticated(request) or request.user.is_authenticated():
      apply.modify_apply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes=data["notes"],
      #apply.modify_apply(name=data['name'],describe= (data['describe']),qps=data['qps'],capacity=data['capacity'],notes="#dep:%s corp:%s\n%s"%(sso_user_get_dep(request),sso_user_get_corp(request) ,data["notes"]),
        cache_or_durable=data['cache_or_durable'],restful_api=data['restful_api'],trade_critical=data['trade_critical'],
        data_source=data['data_source'],complicate_datastruct=data['complicate_datastruct'],entry_num=data["entry_num"],
        used_tair_before=data['used_tair_before'], create_by_username=applicant, modify_by_username=sso_user_get_username(request),
        modify_at=datetime.now(), email=applicant_mail,)
  return HttpResponseRedirect('/app')

def editReivew(request, review_id):
  if not request.user.is_authenticated() and not sso_user_is_authenticated(request) :
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  if len(AdminGroup.objects.filter(username=sso_user_get_username(request))) != 1 and not request.user.is_authenticated():
    error = u'对不起，%s 您没有审批权限, 需要开通请联系Tair答疑'%sso_user_get_username(request)
    return render_to_response('alert.html',{"text":error},context_instance=RequestContext(request))

@csrf_exempt
def modifyImportant(request, app_id):
  if request.method == 'POST':
    important = request.POST.get("i","0")
    app_info = get_object_or_404(App, pk=app_id)
    app_info.set_important_level(important)
  return HttpResponse("ok") 
  
