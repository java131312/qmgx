#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import md5
import io
import json
from opd import models
from opd import command
from django.utils import timezone
from datetime import date, datetime
from django.core import serializers
from django.core.context_processors import request
import command
from django.db import transaction
from opd.publicserver.power import powercheck
@powercheck
def cronttab(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        hostlist=request.REQUEST.getlist('hostbox')
        name=request.POST.get('cronname')
        cronuse=request.POST.get('cronuse')
        m=request.POST.get('cronminute')
        h=request.POST.get('cronhour')
        d=request.POST.get('cronday')
        yue=request.POST.get('cronmonth')
        w=request.POST.get('cronweek')
        hoststr=''
        if not m and not h and not d and not yue and not w:
            print 'error'
        if not w:
            w='*'
        if not m:
            m='*'
        if not h:
            h='*'
        if not d:
            d='*'
        if not yue:
            yue='*'
        content=request.POST.get('croncontent')
        cronresult="name='%s' job='%s' minute='%s' hour='%s' day='%s' month='%s' weekday='%s' " %(name,content,m,h,d,yue,w)
        try:
            with transaction.atomic():
                querysetlist=[]
                for item in hostlist:
                    hostServer=models.Server.objects.get(ipaddrs=item)
                    username=hostServer.account
                    password=hostServer.passwd
                    server_id=hostServer.id
                    server_ip=hostServer.ipaddrs
                    hoststr+=server_ip+','
                    allcount=models.crontab.objects.filter(server_id=server_id).count()
                    if allcount!=0:
                        oldcronname=models.crontab.objects.filter(server_id=server_id)
                        for item in oldcronname:
                            if item.cronname==name and item.deltype==0:
                                raise NameError("duplicate name")  
                        loginusername=user_dict['user']
                        querysetlist.append(models.crontab(server_id=server_id,cronname=name,crontime=m+' '+h+' '+d+' '+yue+' '+w,croncontent=content,crondis=cronuse,cronuser=models.User.objects.get(username=loginusername),deltype=0))
                    else:
                        loginusername=user_dict['user']
                        querysetlist.append(models.crontab(server_id=server_id,cronname=name,crontime=m+' '+h+' '+d+' '+yue+' '+w,croncontent=content,crondis=cronuse,cronuser=models.User.objects.get(username=loginusername),deltype=0))
                for item in hostlist:
                    hostServer=models.Server.objects.get(ipaddrs=item)
                    username=hostServer.account
                    password=hostServer.passwd
                    item=[item]
                    Runobj=command.Modulehandle(item,username,password,cronresult)
                    Runmessages=Runobj.run()
                models.crontab.objects.bulk_create(querysetlist)
                hoststr=hoststr.rstrip(',')
                applyuser=user_dict['user']
                models.opdlog.objects.create(describe='任务内容为:%s' %(content),contentsorfilename='【添加】任务名称为:%s' %(name),approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=5),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
                return render_to_response('opd/success/cron_success.html',{'username':user_dict['user']})
        except Exception,e:
            print e.message
            return HttpResponse('重复了任务名或者报错了，赶紧检查吧。。。')
    if user_dict:
        #allhost=models.Server.objects.all()
        allidc=models.IDC.objects.all()
        return render_to_response('opd/ansible/cron_all.html',{'allidc':allidc,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def cronlist(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        loginusername=user_dict['user']
        loginusername_id=models.User.objects.get(username=loginusername).id
        crontablist=models.crontab.objects.filter(cronuser_id=loginusername_id,deltype=0).order_by('server_id')
        #crontablist.query.group_by=['server_id']
        return render_to_response('opd/ansible/cron_list.html',{'crontablist':crontablist,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def crondel(request):
    ret={'status':''}
    user_dict=request.session.get('is_login',None)
    hoststr=''
    if user_dict and request.method=='POST':
        try:
            delid=request.POST.get('nid')
            cronname=models.crontab.objects.get(id=delid).cronname
            croncontent=models.crontab.objects.get(id=delid).croncontent
            print croncontent
            serverip=models.Server.objects.get(id=models.crontab.objects.get(id=delid).server_id).ipaddrs
            username=models.Server.objects.get(ipaddrs=serverip).account
            password=models.Server.objects.get(ipaddrs=serverip).passwd
            cronresult="name='%s' state=absent" %(cronname)
            Runobj=command.Modulehandle([serverip],username,password,cronresult)
            Runmessages=Runobj.run()
            delresult=models.crontab.objects.get(id=delid)
            delresult.deltype=1
            delresult.save()
            ret['status']=1
            hoststr+=serverip+','
            hoststr=hoststr.rstrip(',')
            applyuser=user_dict['user']
            models.opdlog.objects.create(describe='任务内容为:%s' %(croncontent),contentsorfilename='【删除】任务名称为:%s' %(cronname),approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=5),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
        except Exception,e:
            ret['status']=0
            print e.message
        return HttpResponse(json.dumps(ret))
    else:
        return redirect('/login/')
@powercheck
def modcrontab(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='GET':
        id=request.GET.get('id')
        result=models.crontab.objects.filter(id=id)
        return render_to_response('opd/ansible/cron_modify.html',{'id':id,'result':result,'username':user_dict['user']})
    if user_dict and request.method=='POST':
        id=request.POST.get('crondid')
        name=request.POST.get('cronname')
        cronuse=request.POST.get('cronuse')
        m=request.POST.get('cronminute')
        h=request.POST.get('cronhour')
        d=request.POST.get('cronday')
        yue=request.POST.get('cronmonth')
        w=request.POST.get('cronweek')
        hoststr=''
        if not m and not h and not d and not yue and not w:
            print 'error'
        if not w:
            w='*'
        if not m:
            m='*'
        if not h:
            h='*'
        if not d:
            d='*'
        if not yue:
            yue='*'
        content=request.POST.get('croncontent')
        try:
            with transaction.atomic():
                hostServer=models.Server.objects.get(id=models.crontab.objects.get(id=id).server_id)
                username=hostServer.account
                password=hostServer.passwd
                server_id=hostServer.id
                server_ip=hostServer.ipaddrs
                updis=models.crontab.objects.get(id=id)
                croncontent=updis.croncontent
                cronname=updis.cronname
                cronresult="name='%s' state=absent" %(updis.cronname)
                Runobj=command.Modulehandle([server_ip],username,password,cronresult)
                Runmessages=Runobj.run()
                cronresult="name='%s' job='%s' minute='%s' hour='%s' day='%s' month='%s' weekday='%s' " %(name,content,m,h,d,yue,w)
                Runobj=command.Modulehandle([server_ip],username,password,cronresult)
                Runmessages=Runobj.run()
                updis.cronname=name
                updis.crondis=cronuse
                updis.crontime=m+' '+h+' '+d+' '+yue+' '+w
                updis.croncontent=content
                updis.save()
                hoststr+=server_ip+','
                hoststr=hoststr.rstrip(',')
                applyuser=user_dict['user']
                models.opdlog.objects.create(describe='原任务内容为%s,修改后任务内容为:%s' %(croncontent,content),contentsorfilename='【修改】原任务名称为%s,修改名称后为:%s' %(cronname,name),approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=5),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
                return render_to_response('opd/success/cron_mdsuccess.html',{'username':user_dict['user']})
        except Exception,e:
            print e.message
            return HttpResponse('任务修改失败了，请查明原因再修改')
    else:
        return redirect('/login/') 
@powercheck
def getcrontabtime(request):
    ret={'status':'','data':''}
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='GET':
        try:
            id=request.GET.get('id')
            result=models.crontab.objects.get(id=id).crontime
            ret['status']=1
            ret['data']=result
            return HttpResponse(json.dumps(ret))
        except Exception,e:
           ret['status']=0
           return HttpResponse(json.dumps(ret))
    else:
        ret['status']=0
        return HttpResponse(json.dumps(ret)) 