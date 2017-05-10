#coding:utf-8
import paramiko
class client():
    def __init__(self,idc,ip,account,pwd):
        self.Idc=idc
        self.Ip=ip
        self.Account=account
        self.Pwd=pwd
    @property
    def start(self):
        try:
            paramiko.util.log_to_file('syslogin.log')
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.Ip,port=22,username=self.Account, password=self.Pwd)
            ssh.close()
            return True
        except Exception,e:
            return False