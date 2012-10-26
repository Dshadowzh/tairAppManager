# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from tairAppManager.app.models import ChangeLog, Feedback, AdminGroup
from django.views.decorators.csrf import csrf_exempt

#feedback page
def feedback(request):
  log = ChangeLog.objects.all().order_by("-id")
  fb = Feedback.objects.all().order_by("-id")
  return render_to_response('feedback.html', {"logs":log, "feedbacks":fb},context_instance=RequestContext(request))

def addFeedback(request):
  pass

#mail page
@csrf_exempt
def saveClipBoard(request):
  if request.method == 'POST':
    username = request.POST.get("username", "")
    text = request.POST.get("text", "")
    #print "here", username, text
    admin = get_object_or_404(AdminGroup, username = username)
    admin.clipboard = text
    admin.save()
  return HttpResponse("")

#keyboard control helper
