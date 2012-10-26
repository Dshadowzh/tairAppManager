"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

test for tair Restful interface
"""

from django.test import TestCase
import httplib

class SimpleTest(TestCase):
  
#  def test_base(self):
#    response = self.client.get('/cluster/')
#    #print response.content
#    #print response
#    #print response.status_code

#  def test_alloc_namespace_base(self):
#    area_ke\ = "testxx"
#    quota = 1000
#    print '/openapi/area/%s?type=alloc1&quota=%d'%(area_key, quota)
#    response = self.client.post('/openapi/area/%s'%area_key, {"type":"alloc1", "quota":quota})
#    self.assertEqual(response.status_code, 200)
#    #print response.content

#    response = self.client.post('/openapi/area/%s?type=alloc0&quota=%d'%(area_key+'b', quota))
#    self.assertEqual(response.status_code, 200)
#    print response.content

#  def test_modify_quota_base(self):
#    area_key = "test"
#    quota = 2000
#    response = self.client.post('/openapi/area/%s?type=modify&quota=%d'%(area_key, quota))
#    self.assertEqual(response.status_code, 200)
#
#  def test_delete_quota_base(self):
#    area_key = "test"
#    quota = 2000
#    response = self.client.delete('/openapi/area/%s')
#    self.assertEqual(response.status_code, 200)
#
  def test_get_area_base(self):
    area_key = "test"
    response = self.client.get('/openapi/area/%s?type=cluster'%area_key)
    #response = self.client.get('/openapi/area/%s', {"type":"cluster"})
    print response#.content
    #self.assertEqual(response.status_code, 200)
    response = self.client.get('/openapi/area/%s?type=stat'%area_key)
    print response#.content
    #self.assertEqual(response.status_code, 200)
