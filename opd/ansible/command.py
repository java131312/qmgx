#coding:utf-8
from public import *
'''
import ansible.runner
'''
class Modulehandle():
    def __init__(self,hosts,username,password,cronresult):
        self.username=username
        self.password=password
        self.reuslt=cronresult
        self.ipaddress=hosts
        self.hosts=ansible.inventory.Inventory(self.ipaddress)
        print self.reuslt
    def run(self):
        try:
            self.Runresult = ansible.runner.Runner(
                #pattern='self.hosts',
                remote_user='%s' %(self.username),
                remote_pass='%s' %(self.password),
                forks=10,
                module_name='cron', 
                inventory=self.hosts,
                #module_args="name='wocao' job='/bin/touch /tmp/test.txt >>/dev/null' minute='%s' hour='%s' day='%s' month='%s' weekday='%s' " %(self.minute,self.hour,self.day,self.yue,self.week)
                module_args=self.reuslt
               # module_args="name='gutianyu' state=absent"
                ).run()
            if len(self.Runresult['dark']) == 0 and len(self.Runresult['contacted']) == 0:
                return "no host"
        except Exception,e:
            return str(e)
        return self.Runresult