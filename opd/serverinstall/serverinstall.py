#coding:utf-8
from __future__ import with_statement 
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.db.models.query import QuerySet
import paramiko
import md5
import io
import json
from opd import models
import installcmd
from django.db import transaction
import checknrpe
from opd.tasks import *
from opd.publicserver.power import powercheck
@powercheck
def serverinstall(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        typeid=request.POST.get('typeid')
        if typeid==None:
            hostbox=request.REQUEST.getlist('hostbox')
            serverid=request.POST.get('allserver')
            installdis=request.POST.get('installdis')
            servername=models.serverinstall.objects.get(id=serverid)
            servername=servername.installservername
            loginusername=user_dict['user']
            with transaction.atomic():
                    querysetlist=[]
                    for item in hostbox:
                        hostServer=models.Server.objects.get(id=item)
                        username=hostServer.account
                        password=hostServer.passwd
                        serveripaddr=hostServer.ipaddrs
                        hostname=hostServer.hostname
                        serverobj=models.serverinstall.objects.get(installservername=servername)
                        serverresult=models.Hostserver.objects.filter(servername_id=item).count()
                        haveresult=models.Hostserver.objects.filter(servername_id=item,installhost__installservername=servername).count()
                        #alivenrpe=checknrpe.check_aliveness(serveripaddr,5666)
                        #check_aliveness.delay(serveripaddr,5666)
                        #print alivenrpe
                        if haveresult ==1:
                            raise NameError("already install")
                        if serverresult==1:
                            childobj=models.Hostserver.objects.get(servername_id=item)
                            childobj.installhost.add(serverobj)
                        else:
                            childobj=models.Hostserver.objects.create(servername_id=item)
                            childobj.installhost.add(serverobj)
                        models.Hostinstalldetail.objects.create(hostmachine=models.Server.objects.get(id=item),servername=models.serverinstall.objects.get(id=serverid),installdis=installdis,installuser=models.User.objects.get(username=loginusername),installstatus_id=3)
            install_aliveness.delay(hostbox,serverid)
            #install_aliveness(hostbox,serverid)
            print hostbox,serverid
            '''
            for item in hostbox:
                hostServer=models.Server.objects.get(id=item)
                username=hostServer.account
                password=hostServer.passwd
                serveripaddr=hostServer.ipaddrs
                hostname=hostServer.hostname
                item=[item]
                Runobj=installcmd.Installserver([serveripaddr],username,password,servername,hostname)
                abc=Runobj.ansible_playbook.delay()
              '''
            return HttpResponse('正在安装，请稍后到安装详情页面查看')
        else:
            ret={'status':''}
            try:
                ret['status']=1
                print 'ok'
                return HttpResponse(json.dumps(ret))
            except Exception,e:
                ret['status']=0
                return HttpResponse(json.dumps(ret))
    elif user_dict:
        #allhost=models.Server.objects.all()
        allidc=models.IDC.objects.all()
        allserver=models.serverinstall.objects.all()
        return render_to_response('opd/ansible/serverinstall.html',{'allserver':allserver,'allidc':allidc,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def serverdetail(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        ret={'status':'','data':''}
        serverid=request.POST.get('nid')
        hostresult=models.Hostinstalldetail.objects.filter(hostmachine_id=serverid).values('id','hostmachine','servername','servername__installservername','installdis','installstatus','installstatus__hoststatus')
        hostresult=list(hostresult)
        ret['data']=hostresult
        try:
            return HttpResponse(json.dumps(ret))
        except Exception,e:
            print e.message
    elif user_dict:
        hostserver=models.Hostserver.objects.all()
        #hostserver=models.Hostinstalldetail.objects.all()
        #hostserver.query.group_by=['hostmachine_id']
        #print hostserver
        #detailhostserver=models.Hostserver.objects.get(servername_id=22)
        #detailhostserver=detailhostserver.installhost.all()
       # detailhostserver=models.Hostinstalldetail.objects.filter(hostmachine_id=22)
        return render_to_response('opd/ansible/server_detail.html',{'hostserver':hostserver,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def serveropd(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        ret={'status':'','data':''}
        hostid=request.POST.get('hostid')
        serverid=request.POST.get('serverid')
        typeid=request.POST.get('typeid')
        servername=models.serverinstall.objects.get(id=serverid)
        servername=servername.installservername
        loginusername=user_dict['user']
        with transaction.atomic():
            hostServer=models.Server.objects.get(id=hostid)
            username=hostServer.account
            password=hostServer.passwd
            serveripaddr=hostServer.ipaddrs
            hostname=hostServer.hostname
            Runobj=installcmd.Installserver([serveripaddr],username,password,servername,hostname)
            if typeid=='1':
                abc=Runobj.nrpe_start()
                if abc==False:
                    ret['status']=1
                    ret['data']=1
                    return HttpResponse(json.dumps(ret))
                if abc[serveripaddr]['unreachable']>=1 or abc[serveripaddr]['failures']>=1:
                    ret['status']=1
                    ret['data']=1
                else:
                    flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=hostid),servername=models.serverinstall.objects.get(id=serverid))
                    flushstatus.installstatus_id=1
                    flushstatus.save()
                    ret['status']=0
                    ret['data']=1
            elif typeid=='2':
                abc=Runobj.nrpe_reboot()
                print abc
                if abc[serveripaddr]['unreachable']>=1 or abc[serveripaddr]['failures']>=1:
                    ret['status']=1
                    ret['data']=2
                else:
                   ret['status']=0 
                   ret['data']=2
            else:
                abc=Runobj.nrpe_stop()
                print abc
                if abc[serveripaddr]['unreachable']>=1 or abc[serveripaddr]['failures']>=1:
                    ret['status']=1
                    ret['data']=3
                else:
                    flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=hostid),servername=models.serverinstall.objects.get(id=serverid))
                    flushstatus.installstatus_id=2
                    flushstatus.save()
                    ret['status']=0
                    ret['data']=3
            return HttpResponse(json.dumps(ret))
@powercheck
def getinstalldis(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        try:
            ret={'status':'','data':''}
            hostid=request.POST.get('hostid')
            serverid=request.POST.get('serverid')
            disresult=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=hostid),servername=models.serverinstall.objects.get(id=serverid))
            ret['data']=disresult.installdis
            ret['status']=1
        except Exception,e:
            ret['status']=0
        return HttpResponse(json.dumps(ret))