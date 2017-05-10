#coding:utf-8
#import ansible.runner
'''
import ansible
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

vars = "hello world"
ansible_command = "/usr/local/bin/ansible-playbook"
playbook = "/root/playbook/"
#hosts = ['192.168.0.5']

# Boilerplace callbacks for stdout/stderr and log output
#utils.VERBOSITY = 0
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
stats = callbacks.AggregateStats()
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
'''
class Installserver():
    def __init__(self,hosts,username,password,serverinstall,hostname):
        self.username=username
        self.password=password
        self.server=serverinstall
        self.ipaddress=hosts
        self.hostname=hostname
    def ansible_playbook(self):
        try:
            self.Runresult = PlayBook(
                playbook=playbook+'%s/%s.yml' %(self.server,self.server),
                inventory = Inventory(self.ipaddress), 
                callbacks = playbook_cb,
                runner_callbacks = runner_cb,
                remote_user='%s' %(self.username),
                remote_pass='%s' %(self.password),
                stats = stats,
                check = False,
                #extra_vars = {'var':"%s" %(self.hostname)}
                )
            return self.Runresult.run()
            #if len(self.Runresult['dark']) == 0 and len(self.Runresult['contacted']) == 0:
            #    return "no host"
        except Exception,e:
            print str(e)
            return False
        #return self.Runresult
    def nrpe_reboot(self):
        try:
            self.Runresult = PlayBook(
                playbook=playbook+'%s/%sreboot.yml' %(self.server,self.server),
                inventory = Inventory(self.ipaddress), 
                callbacks = playbook_cb,
                runner_callbacks = runner_cb,
                remote_user='%s' %(self.username),
                remote_pass='%s' %(self.password),
                stats = stats,
                check = False,
                #extra_vars = {'var':"%s" %(self.hostname)}
                )
            return self.Runresult.run()
            #if len(self.Runresult['dark']) == 0 and len(self.Runresult['contacted']) == 0:
            #    return "no host"
        except Exception,e:
            print str(e)
            return False
    def nrpe_stop(self):
        try:
            self.Runresult = PlayBook(
                playbook=playbook+'%s/%sstop.yml' %(self.server,self.server),
                inventory = Inventory(self.ipaddress), 
                callbacks = playbook_cb,
                runner_callbacks = runner_cb,
                remote_user='%s' %(self.username),
                remote_pass='%s' %(self.password),
                stats = stats,
                check = False,
                #extra_vars = {'var':"%s" %(self.hostname)}
                )
            return self.Runresult.run()
            #if len(self.Runresult['dark']) == 0 and len(self.Runresult['contacted']) == 0:
            #    return "no host"
        except Exception,e:
            print str(e)
            return False
    def nrpe_start(self):
        try:
            self.Runresult = PlayBook(
                playbook=playbook+'%s/%sstart.yml' %(self.server,self.server),
                inventory = Inventory(self.ipaddress), 
                callbacks = playbook_cb,
                runner_callbacks = runner_cb,
                remote_user='%s' %(self.username),
                remote_pass='%s' %(self.password),
                stats = stats,
                check = False,
                #extra_vars = {'var':"%s" %(self.hostname)}
                )
            return self.Runresult.run()
            #if len(self.Runresult['dark']) == 0 and len(self.Runresult['contacted']) == 0:
            #    return "no host"
        except Exception,e:
            print str(e)
            return False