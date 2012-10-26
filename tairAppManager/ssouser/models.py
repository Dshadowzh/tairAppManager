from django.db import models
from django.contrib.auth.models import Group
import sys,urllib

class MyUser(models.Model):
  user_name = models.CharField(max_length=30)
  user_emp_id = models.IntegerField()
  user_id = models.IntegerField()
  user_tel = models.CharField(max_length=20)
  user_depart = models.CharField(max_length=50)
  user_email= models.EmailField(default="")
  #auth_user= models.ForeignKey(User, null=True, blank=True)
  group = models.ForeignKey(Group ,null=True, blank=True)

  
def sso_user_is_authenticated(request):
  #print >> sys.stderr, request,request.META.get("SSO_USERID","") and True or False
  return request.META.get("SSO_USERID","") and True or False

def sso_user_get_uid(request):
  return request.META.get("SSO_USERID","")

def sso_user_get_username(request):
  name = request.META.get("SSO_CNAME","") or request.user.username
  #print >> sys.stderr, name
  return urllib.unquote(name).split("(")[0]

def sso_user_get_tel(request):
  return request.META.get("SSO_TEL","") 

def sso_user_get_empid(request):
  tbsso = request.COOKIES.get("TBSSO","") 
  if not tbsso:
    return request.user.id
  u = urllib.unquote(tbsso)
  return urllib.unquote(u.split("&employeeid=")[1].split("&corp=")[0])

def sso_user_get_userid(request):
  return request.META.get("SSO_USERID","")

def sso_user_get_email(request):
  tbsso = request.COOKIES.get("TBSSO","") 
  if not tbsso:
    return request.user.email
  u = urllib.unquote(tbsso)
  return urllib.unquote(u.split("&email=")[1].split("&")[0])

def sso_user_get_corp(request):
  tbsso = request.COOKIES.get("TBSSO","") 
  if tbsso=="":
    return ""
  u = urllib.unquote(tbsso)
  return urllib.unquote(u.split("&corp=")[1].split("&tel=")[0])

def sso_user_get_dep(request):
  tbsso = request.COOKIES.get("TBSSO","") 
  if tbsso=="":
    return ""
  u = urllib.unquote(tbsso)
  return urllib.unquote(u.split("&dep=")[1].split("&param=")[0])

def create_sso_user(request):
  u = MyUser(user_name=sso_user_get_username(request),user_emp_id=sso_user_get_emp(request), 
      user_depart=sso_user_get_dep(request),user_email=sso_user_get_email(request),
      user_id=sso_user_get_uid(request),user_tel=sso_user_get_telr(request))
  u.save()
  return  

admin_type=(('3', "root"), ('2', "reviewr"), ('1', "applicant"))

class MyGroup(models.Model):
  user_id = models.CharField(max_length=30, primary_key=True)
  group = models.CharField(max_length=1, choices = admin_type)
   
def check():
  pass
