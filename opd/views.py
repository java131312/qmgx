#coding:utf-8
from __future__ import with_statement 
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.db.models.query import QuerySet
import paramiko
import md5
import io
import os
import json
import models
from django.utils.safestring import mark_safe
from opd import command, pageinfo
from django.utils import timezone
from datetime import date, datetime,timedelta
from django.core import serializers
from django.core.context_processors import request
from opd.sftp import allconf
from opd.pageinfo import commd
from opd.pageinfo import html_page
import ConfigParser
import codecs
from opd.publicserver.power import powercheck
from _ast import Num
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.
def testfile(request):
    if request.method=='GET':
        return render_to_response('opd/manyfile.html')
        print 'GET'
    if request.method=='POST':
        filename=request.FILES['Filedata'].name
        user_upload_folder='D:\\'
        file_upload=open(os.path.join(user_upload_folder,filename),'w')
        file_upload.write(request.FILES['Filedata'].read())
        return render_to_response('opd/manyfile.html')
def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
		#logger.info(password)
	logging.debug('This is debug message--------')
        logging.info('test a debug---')
        logging.debug(username)
        
        logging.debug(password)
        md5password=md5.new()
        md5password.update(password)
        newpassword=md5password.hexdigest()
        try:
            currentObj=models.User.objects.get(username=username,password=newpassword)
            logging.debug(currentObj)
            permission=currentObj.user_type_id
            request.session['is_login']={'user':username}
            request.session['permission']={'permi':permission}
        except Exception,e:
            currentObj=None
        if currentObj:
            request.session['current_user_id']=currentObj.id
            if permission==1:
                return redirect('/index/')
            else:
                return redirect('/index2/')
        else:
            return redirect('/login/')
    return render_to_response('opd/login.html')
def loginout(request):
    ret={'status':0,'message':''}
    try:
        del request.session['is_login']
        ret['status']=1
    except Exception,e:
        ret['message']=e.message
    return redirect('/login/')
def modifypasswd(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        oldpwd=request.POST.get('usernameoldpwd')
        newpwd=request.POST.get('usernamenewpwd')
        cfmpwd=request.POST.get('usernamecfmpwd')
        username=user_dict['user']
        nowpwd=models.User.objects.get(username=username)
        pwd=nowpwd.password
        md5password=md5.new()
        md5password.update(newpwd)
        newpassword=md5password.hexdigest()
        oldmd5pwd=md5.new()
        oldmd5pwd.update(oldpwd)
        oldmd5pwd=oldmd5pwd.hexdigest()
        if newpwd==cfmpwd and pwd==oldmd5pwd:
            nowpwd.password=newpassword
            nowpwd.save()
            return redirect('/login/')
        else:
            return HttpResponse('操作有误请重新操作')
    else:
        return redirect('/login/')  
@powercheck
def index(request):
    config=ConfigParser.ConfigParser()
    #with codecs.open(r'./qmgx/opd/config.conf','r+',encoding='utf-8') as cfgfile:
    #    config.readfp(cfgfile)
    #localpath=config.get("global","getlocalpath")
   # print localpath
        #print config.get('global','port')
        #print config.get('global','password')
    user_dict=request.session.get('is_login',None)
    if user_dict:
        allcount=models.Server.objects.all().count()
        allclick=models.Crtnumber.objects.all()
        allnumber=0
        for i in allclick:
            allnumber+=int(i.number)
        now=datetime.now()
        delta=timedelta(hours=-24)
        n_days=now+delta
        n_days=n_days.strftime('%Y-%m-%d %H:%M:%S')
        thallclick=models.Crtnumber.objects.filter(create_at__gte=n_days)
        thallnumber=0
        for i in thallclick:
            thallnumber+=int(i.number)
        return render_to_response('opd/index.html',{'thallnumber':thallnumber,'allnumber':allnumber,'allcount':allcount,'username':user_dict['user']})
    else:
        return redirect('/login/')
def index2(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        allcount=models.Server.objects.all().count()
        return render_to_response('opd/index2.html',{'allcount':allcount,'username':user_dict['user']})
    else:
        return redirect('/login/')
@powercheck
def hostlist(request,page):
    user_dict=request.session.get('is_login',None)
    ulid=request.GET.get('ulid')
    liid=request.GET.get('liid')
    if user_dict:
        per_item=commd.try_int(request.COOKIES.get('pager_num',5),5)
        page=commd.try_int(page, 1)
        allhost=models.Server.objects.all().count()
        hostpageObj=html_page.PageInfo(page,allhost,per_item)
        allroom=models.IDC.objects.all()
        allhost=models.Server.objects.all()[hostpageObj.start:hostpageObj.end]
        page_string=html_page.Pager(page, hostpageObj.all_page_count)
        response=render_to_response('opd/tables_static.html',{'page':page_string,'ulid':ulid,'liid':liid,'allroom':allroom,'allhost':allhost,'username':user_dict['user']})
        response.set_cookie('pager_num',per_item)
        return response
    else:
        return redirect('/login/')
@powercheck
def mdgetidc(request):
    ret={'status':0,'data':''}
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        try:
            idcresult=models.IDC.objects.all()
            result=[]
            for i in idcresult:
                result.append({'id':i.id,'name':i.housename})
                #group.append(i.groupname)
            ret['status']=1
            ret['data']=result
            #return render_to_response('opd/tables_static.html',{'allhostgroup':currentgroup})
            return HttpResponse(json.dumps(ret))
        except Exception,e:
            ret['status']=0
            print e.message
@powercheck
def mdhostinfo(request):
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        id=request.POST.get('hostid')
        mdhostname=request.POST.get('mdhostname')
        mdhouseroomid=request.POST.get('mdhouseroomid')
        mdhousegroupid=request.POST.get('mdhousegroupid')
        hostobj=models.Server.objects.get(id=id)
        hostobj.hostname=mdhostname
        hostobj.house_id=mdhouseroomid
        hostobj.servergroup_id=mdhousegroupid
        hostobj.save()
        return redirect('/list/')
        #print id,mdhostname,mdhouseroomid,mdhousegroupid
@powercheck
def getgroup(request):
    ret={'status':0,'data':''}
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        try:
            housegroupid=request.POST.get('nid')
            hostgroup=models.IDC.objects.get(id=housegroupid)
            currentgroup=hostgroup.hostgroup.all()
            group=[]
            for i in currentgroup:
                group.append({'id':i.id,'name':i.groupname})
                #group.append(i.groupname)
            ret['status']=1
            ret['data']=group
            #return render_to_response('opd/tables_static.html',{'allhostgroup':currentgroup})
            return HttpResponse(json.dumps(ret))
        except Exception,e:
            ret['status']=0
            print e.message
       #for i in hostgroup:
       #    print i
@powercheck
def gethost(request):
    ret={'status':0,'data':''}
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        try:
           idcid=request.POST.get('idcid')
           groupid=request.POST.get('groupid')
           servername=models.Server.objects.filter(house_id=idcid,servergroup_id=groupid).values('id','hostname','ipaddrs')
           servername=list(servername)
           ret['status']=1
           ret['data']=servername
           return HttpResponse(json.dumps(ret))
        except Exception,e:
           ret['status']=0
           print e.message 
@powercheck
def addhost(request):
    ret={'status':0}
    houseroomid=request.POST.get('houseroomid')
    housegroupid=request.POST.get('housegroupid')
    hostusername=request.POST.get('hostusername')
    ipaddr=request.POST.get('ipaddr')
    hostpwd=request.POST.get('hostpwd')
    hostname=request.POST.get('hostname')
    hostObj=command.client(houseroomid,ipaddr,hostusername,hostpwd)
    result=hostObj.start
    time=datetime.now()
    if result:
        ret['status']=1
        ipaddr=models.Server.objects.create(servergroup_id=housegroupid,house=models.IDC.objects.get(id=houseroomid),hostname=hostname,ipaddrs=ipaddr,account=hostusername,passwd=hostpwd,update_at=time)
        return redirect('/list')
    else:
        ret['status']=0
        return HttpResponse('新增错误')
@powercheck
def hostcheck(request):
    ret={'id':''}
    id=request.POST.get('nid')
    chatlist=models.Server.objects.filter(id=id)
    for item in chatlist:
         backid=item.status_id
         ret['id']=backid
    return HttpResponse(json.dumps(ret))
@powercheck
def delhost(request):
    ret={'status':''}
    try:
        id=request.POST.get('nid')
        models.Server.objects.get(id=id).delete()
        ret['status']=1
    except Exception,e:
        ret['status']=0
    return HttpResponse(json.dumps(ret))
@powercheck
def delallhost(request):
    ret={'status':0,'data':''}
    user_dict=request.session.get('is_login',None)
    if user_dict and request.method=='POST':
        delid=request.REQUEST.getlist('nid')
        hostbox=''.join(delid)
        hostbox=hostbox.rstrip(',')
        try:
            models.Server.objects.extra(where=['id IN('+hostbox+')']).delete()
            ret['status']=1
        except Exception,e:
            print e.message
            ret['status']=0
        return HttpResponse(json.dumps(ret))
@powercheck
def read(request):
    ret={'data':''}
    output=open(r'C:\Users\gty\test.txt')
    content=output.readlines()
    content=''.join(content)
    ret['data']=content
    output.close()
    return HttpResponse(json.dumps(ret))
@powercheck
def fileread(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        allidc=models.IDC.objects.all()
        #allhost=models.Server.objects.all()
        return render_to_response('opd/form_components.html',{'allidc':allidc,'username':user_dict['user']})
    else:
        return redirect('/login/')
