#coding:utf-8
'''
Created on 2016年11月14日

@author: gty
'''
import paramiko
import os
import signal
import  subprocess
import  time
class client():
    def __init__(self,ip,account,pwd,command,service):
        self.Ip=ip
        self.Account=account
        self.Pwd=pwd
        self.command=command
        self.service=service
    @property
    def start(self):
        try:
            paramiko.util.log_to_file('syslogin.log')
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Ip,port=22,username=self.Account, password=self.Pwd)
            stdin,stdout,stderr=ssh.exec_command(self.command)
            result=stdout.read()
            ssh.close()
            if self.command:
                return '=========================================================================\n'+'['+self.Ip+'--'+self.service+'~]#'+self.command+'\n'+'=========================================================================\n',result
            else:
                return '['+self.Ip+self.service+'~]#'+'not found  command,please enter.\n'
        except Exception,e:
            print e.message
            return '['+self.Ip+self.service+'~]#'+'host connect fail.\n'
    @property
    def servierdir(self):
        try:
            paramiko.util.log_to_file('syslogin.log')
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Ip,port=22,username=self.Account, password=self.Pwd)
            stdin,stdout,stderr=ssh.exec_command(self.command)
            result=stdout.read()
            ssh.close()
            if self.command:
                return result
            else:
                return '['+self.Ip+self.service+'~]#'+'not found  command,please enter.\n'
        except Exception,e:
            print e.message
            return '['+self.Ip+self.service+'~]#'+'host connect fail.\n'
    @property
    def logcountnumber(self):
        try:
            paramiko.util.log_to_file('syslogin.log')
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Ip,port=22,username=self.Account, password=self.Pwd)
            stdin,stdout,stderr=ssh.exec_command(self.command)
            result=stdout.read()
            ssh.close()
            if self.command:
                return result
            else:
                return 'error'
        except Exception,e:
            print e.message
            return 'error'