from tairAppManager.ssouser.models import *

def ssoUserAdd(request):
  username=sso_user_get_username(request)
  return {'username': username}
