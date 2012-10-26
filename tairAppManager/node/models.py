from django.db import models
from tairAppManager.cluster.models import Cluster

# Create your models here.

class Node(models.Model):
  name = models.TextField()
  ip = models.CharField(max_length = 16)
  rack = models.CharField(max_length = 30)
  model = models.CharField(max_length = 30)
  os = models.CharField(max_length = 30)
  type = models.TextField()

  cluster = models.ForeignKey(Cluster)  

  def __unicode__(self):
    return u'%d) %s/%s'%(self.id, self.cluster.cluster_name, self.name)
