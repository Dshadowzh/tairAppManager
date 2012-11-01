# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import shlex
import re

tair_return_patten={
  "alloc":"alloc successful.  area_num: (?P<area>\d+)\n",
  "modify":"modify quota successful\n",
  "delete":"modify quota successful\n",
  "stat":"",
  "error":"failed with -(?P<error>\d+)",
}

#class dataentry(Structure):
#    _fields_ = [('len',c_int),
#                ('data', c_void_p)]
#    
#class areainfo(Structure):
#    _fields_ = []

class tairclient:
    def __init__(self, master, slave, group, area = 0, client="/home/admin/tair/sbin/tairclient"):
        self.area = area
        #self.cmd_base = "%s -c %s -g %s"%(client, master, group)
        self.cmd_base = [client, '-c', master, '-g', group, '-l']
        
    def __del__(self):
        pass

    def get(self, key, default = None):
        pass

    def put(self, key, val, expire = 0, version = 0):
        pass

    def remove(self, key):
        pass

    def alloc_namespace(self, key, quota):
          #cmd_c=["/home/admin/tair/sbin/tairclient", "-c", "10.249.199.174:5198", "-g", "group_1", "-l", "alloc_namespace sdiii 123"]
        cmd = ['alloc_namespace %s %d'%(key, quota)]
        try:
          s = Popen(self.cmd_base + cmd, stdout=PIPE, stderr=PIPE)
        except OSError:
          print "popen oserror", e
          return -1
        except e:
          print "popen error", e
          return -1

        (output, stderr) = s.communicate() 
        #print "output:", output, "stderr:", stderr
        if re.match(tair_return_patten["error"], stderr):
          print stderr
          return -1
        if re.match(tair_return_patten["alloc"], stderr):
          return re.match(tair_return_patten["alloc"], stderr).groups()[0]
        print "unknown error"
        return -1

    def modify_quota(self, key, quota):
        cmd = ['modify_quota %s %d'%(key, quota)]
        try:
          s = Popen(self.cmd_base + cmd, stdout=PIPE, stderr=PIPE)
        except OSError:
          print "popen oserror", e
          return -1
        except e:
          print "popen error", e
          return -1

        (output, stderr) = s.communicate() 
        #print "output:", output, "stderr:", stderr
        if re.match(tair_return_patten["error"], stderr):
          return -1
        if re.match(tair_return_patten["modify"], stderr):
          return 0
        print "unknown error"
        return -1

    def get_stat(self, key):
        cmd = ['stat']
        try:
          s = Popen(self.cmd_base + cmd, stdout=PIPE, stderr=PIPE)
        except OSError:
          print "popen oserror", e
          return -1
        except e:
          print "popen error", e
          return -1

        (output, stderr) = s.communicate() 
        #print "output:", output, "stderr:", stderr
        patten = ".*area\((?P<area>\d+)\)\s+%s,(?P<quota>\d+).*"%(key)
        res = re.search(patten, stderr)
        stat = ["0"] *8
        area = -1
        if res:
            area = res.groups()[0]
            quota = res.groups()[0]
            patten2 = "\n%s \w+ (\d+)"%area
            r = re.compile(patten2)
            for (i, match) in enumerate(r.finditer(stderr)):
                stat[i]= match.groups()[0]
        return {"areaKey":key, "area":area, "quota":quota, "stat":{"dataSize":stat[0], "evictCount":stat[1], "getCount":stat[2], "hitCount":stat[3], "itemCount":stat[4], "putCount":stat[5], "removeCount":stat[6], "useSize":stat[7]}}

def test():
    tc = tairclient('10.249.199.174:5198', 
                    '10.249.199.184:5198',
                    'group_1')
    
    #tc.put('hello', '12345')
    #print tc.get('hello')
    #tc.remove('hello')
    #assert(tc.get('hello') == None)
    
    #print "@@@ remove" 
    #print tc.modify_quota("abcde",0)
    print "@@@ alloc" 
    area = tc.alloc_namespace("abcdef", 1234)
    print area
    #print "@@@ stat" 
    #print tc.get_stat("abcde")
    print "@@@ modify" 
    print tc.modify_quota("abcdef",3210)
    print "@@@ stst" 
    print tc.get_stat("abcde")
    #print tc.get_stat("abcde")
    #print tc.get_stat("abdf")

if __name__ == '__main__':
    test()
