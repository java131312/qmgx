#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import io
import json
import models
from opd import command
from django.utils import timezone
from datetime import date, datetime
from django.core import serializers
from django.core.context_processors import request
from opd import cmd
from _codecs import encode
from opd.publicserver.power import powercheck
@powercheck
def shellcmd(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        #allhost=models.Server.objects.all()
        allidc=models.IDC.objects.all()
        return render_to_response('opd/shellcmd.html',{'allidc':allidc,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def shellresult(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        applyuser=user_dict['user']
        ret={'data':'','status':''}
        hostbox=request.REQUEST.getlist('data')
        shellcmd=request.POST.get('shellcmd')
        shellcmd=shellcmd.strip()
        shellcmdcheck=shellcmd.split()
        shellcmdcheck=shellcmdcheck[0]
        role=models.Commandcontrol.objects.filter(command__icontains=shellcmdcheck,role_id=models.User.objects.get(username=applyuser).user_type_id).count()
        if role==0:
            hostbox=''.join(hostbox)
            hostbox=hostbox.strip(',')
            hostbox=hostbox.split(',')
            all=[]
            hoststr=''
            for i,item in enumerate(hostbox):
                hostServer=models.Server.objects.get(id=item)
                username=hostServer.account
                password=hostServer.passwd
                hostname=hostServer.ipaddrs
                service=hostServer.hostname
                hoststr+=hostname+','
                hostObj=cmd.client(hostname,username,password,shellcmd,service)
                result=hostObj.start
                result=list(result)
                all+=result
            ret['status']=1
            ret['data']=all
            hoststr=hoststr.rstrip(',')
            models.opdlog.objects.create(contentsorfilename=shellcmd,approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=4),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
            return HttpResponse(json.dumps(ret))
        else:
          ret['status']=0
          return HttpResponse(json.dumps(ret))
    else:
        return redirect('/login/')