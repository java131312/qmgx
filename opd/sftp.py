#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import os
import json
import models
import config
from opd import command
from django.utils import timezone
from datetime import date, datetime
from django.core import serializers
from django.core.context_processors import request
from macpath import split
from forms import UserForm
import ConfigParser
import codecs
from opd import cmd
from opd.publicserver.power import powercheck
# Create your views here.
@powercheck
def getcontent(request):
    ret={'data':'','status':''}
    import paramiko
    serverId=request.POST.get('optionsRadios')
    path=request.POST.get('regular')
    path=path.strip()
    file=path.split('/')[-1]
    hostServer=models.Server.objects.get(id=serverId)
    username=hostServer.account
    password=hostServer.passwd
    hostname=hostServer.ipaddrs
    port=22
    try:
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp=paramiko.SFTPClient.from_transport(t)
        #config=ConfigParser.ConfigParser()
        #with codecs.open(r'./opd/config.conf','r+',encoding='utf-8') as cfgfile:
        #    config.readfp(cfgfile)
        #localpath=config.get("global","getlocalpath")
        localpath=config.Configget().default()
        #sftp.get(path,"C:\Users\gty\Documents\python_study\qmgx\opd\serverfile\%s" %(file))
        sftp.get(path,"%s%s" %(localpath,file))
        t.close()
        output=open(r'%s%s' %(localpath,file),'r+')
        content=output.readlines()
        content=''.join(content)
        ret['data']=content
        output.close()
        ret['status']=0
        os.remove(r'%s%s' %(localpath,file))
        return HttpResponse(json.dumps(ret))
    except Exception,e:
        print str(e) 
        ret['status']=1 
        os.remove(r'%s%s' %(localpath,file))
        return HttpResponse(json.dumps(ret))
@powercheck
def addcontent(request):
    ret={'data':''}
    serverId=request.POST.get('optionsRadios')
    localpath=config.Configget().default()
    path=request.POST.get('regular')
    file=path.split('/')[-1]
    cfgcontent=request.POST.get('textarea')
    hostServer=models.Server.objects.get(id=serverId)
    username=hostServer.account
    password=hostServer.passwd
    hostname=hostServer.ipaddrs
    port=22
    try:
        user_dict=request.session.get('is_login',None)
        applyuser=user_dict['user']
        output=open(r'%s%s' %(localpath,file),'w')
        #content=output.readlines()
        #content=''.join(content)
        cfgcontent=cfgcontent.encode('utf-8')
        output.write(cfgcontent) 
        output.close()
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.put('%s%s' %(localpath,file),path)
        t.close()
        os.remove('%s%s' %(localpath,file))
        models.opdlog.objects.create(contentsorfilename=path,approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=2),applyuser=models.User.objects.get(username=applyuser),hostlist=hostname)
        return render_to_response('opd/success/sigcfgsuccess.html',{'username':user_dict['user']})
    except Exception,e:
         print str(e)   
         return HttpResponse('修改失败了，请排查检查服务器是否连通')
@powercheck
def allconf(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        #allhost=models.Server.objects.all()
        allidc=models.IDC.objects.all()
        return render_to_response('opd/form_all.html',{'allidc':allidc,'username':user_dict['user']})
    return redirect('/login/')
@powercheck
def suballconf(request):
    hostbox=request.REQUEST.getlist('hostbox')
    ret={'data':''}
    import paramiko
    serverId=request.POST.get('optionsRadios')
    localpath=config.Configget().default()
    path=request.POST.get('regular')
    path=path.strip()
    file=path.split('/')[-1]
    serverdir=path[0:len(path)-len(file)]
    shellcmd='ls %s' %(serverdir)
    cfgcontent=request.POST.get('textarea')
    output=open(r'%s%s' %(localpath,file),'w')
    cfgcontent=cfgcontent.encode('utf-8')
    output.write(cfgcontent) 
    output.close()
    hoststr=''
    for allServer in hostbox:
        hostServer=models.Server.objects.get(id=allServer)
        username=hostServer.account
        password=hostServer.passwd
        hostname=hostServer.ipaddrs
        service=hostServer.hostname
        hostObj=cmd.client(hostname,username,password,shellcmd,service)
        result=hostObj.servierdir
        if result == '':
            hostObj=cmd.client(hostname,username,password,'mkdir -p %s' %(serverdir),service)
            result=hostObj.servierdir
            hoststr+=hostname+','
            port=22
            try:
                t=paramiko.Transport((hostname,port))
                t.connect(username=username,password=password)
                sftp=paramiko.SFTPClient.from_transport(t)
                sftp.put('%s%s' %(localpath,file),path)
                t.close()
            except Exception,e:
                print str(e)
                hostname=str(hostname)
                return HttpResponse('失败了，请检查服务器%s是否连通和目录结构是否一样' %(hostname))
        else:
            hoststr+=hostname+','
            port=22
            try:
                t=paramiko.Transport((hostname,port))
                t.connect(username=username,password=password)
                sftp=paramiko.SFTPClient.from_transport(t)
                sftp.put('%s%s' %(localpath,file),path)
                t.close()
            except Exception,e:
                print str(e)
                hostname=str(hostname)
                return HttpResponse('失败了，请检查服务器%s是否连通和目录结构是否一样' %(hostname))
    user_dict=request.session.get('is_login',None)
    applyuser=user_dict['user']
    os.remove('%s%s' %(localpath,file))
    hoststr=hoststr.rstrip(',')
    models.opdlog.objects.create(contentsorfilename=path,approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=2),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
    return render_to_response('opd/success/allcfgsuccess.html',{'username':user_dict['user']})
@powercheck
def fileupload(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        allhost=models.Server.objects.all()
        localpath=config.Configget().upload()
        path=request.POST.get('regular')
        hostbox=request.REQUEST.getlist('hostbox')
        if request.method == "POST":
            uf = UserForm(request.POST,request.FILES)
            if  path=='' and  not uf.is_valid() and len(hostbox)==0:
                return HttpResponse('啥都不做，就提交，我确定你是过来搞笑的！！')
            uf = UserForm(request.POST,request.FILES)
            count=models.Fileupload.objects.all().count()
            if count>0:
                lastid=models.Fileupload.objects.all().order_by("-id")[0]
                currentid=lastid.id+1
                if uf.is_valid():
                    headImg = uf.cleaned_data['headImg']
                    user = models.Fileupload()
                    user.headImg = headImg
                    user.save()
                    currentfile=models.Fileupload.objects.get(id=currentid)
                    newfile=currentfile.headImg
                    newfile=str(newfile)
                    newfile=newfile.split('/')[-1]
                    newfile=newfile.decode('utf-8')
                    hoststr=''
                    if len(hostbox)==0:
                        os.remove('%s%s' %(localpath,newfile))
                        return HttpResponse('主机同步，你不选择同步的主机，你这是想干啥')
                    for allServer in hostbox:
                        hostServer=models.Server.objects.get(id=allServer)
                        username=hostServer.account
                        password=hostServer.passwd
                        hostname=hostServer.ipaddrs
                        hoststr+=hostname+','
                        port=22
                        try:
                            t=paramiko.Transport((hostname,port))
                            t.connect(username=username,password=password)
                            sftp=paramiko.SFTPClient.from_transport(t)
                            try:
                                rightpath=path[len(path)-1]
                            except Exception,e:
                                os.remove('%s%s' %(localpath,newfile))
                                return HttpResponse('输入远程的文件路径以"/"结尾哦')
                            if rightpath=='/':
                                sftp.put('%s%s' %(localpath,newfile),'%s%s' %(path,newfile))
                                t.close()
                            else:
                                os.remove('%s%s' %(localpath,newfile))
                                return HttpResponse('你是玩Linux的吗，不知道路径后面需要有"/"啊，赶紧回去加个杠，文件就不需要你指定了！！哈哈')
                        except Exception,e:
                             os.remove('%s%s' %(localpath,newfile))
                             print str(e)
                             return HttpResponse('失败了，请检查代码。。')
                    os.remove('%s%s' %(localpath,newfile))
                    hoststr=hoststr.rstrip(',')
                    applyuser=user_dict['user']
                    models.opdlog.objects.create(contentsorfilename=newfile,approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=3),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
                    return render_to_response('opd/success/fileuploadsuccess.html')
                else:
                  return HttpResponse('请选择上传的文件，')  
            else:
                if uf.is_valid():
                    headImg = uf.cleaned_data['headImg']
                    user = models.Fileupload()
                    user.headImg = headImg
                    user.save()
                    lastid=models.Fileupload.objects.all().order_by("-id")[0]
                    currentid=lastid.id
                    currentfile=models.Fileupload.objects.get(id=currentid)
                    newfile=currentfile.headImg
                    newfile=str(newfile)
                    newfile=newfile.split('/')[-1]
                    newfile=newfile.decode('utf-8')
                    hoststr=''
                    if len(hostbox)==0:
                        os.remove('%s%s' %(localpath,newfile))
                        return HttpResponse('主机同步，你不选择同步的主机，你这是想干啥')
                    for allServer in hostbox:
                        hostServer=models.Server.objects.get(id=allServer)
                        username=hostServer.account
                        password=hostServer.passwd
                        hostname=hostServer.ipaddrs
                        hoststr+=hostname+','
                        port=22
                        try:
                            t=paramiko.Transport((hostname,port))
                            t.connect(username=username,password=password)
                            sftp=paramiko.SFTPClient.from_transport(t)
                            try:
                                rightpath=path[len(path)-1]
                            except Exception,e:
                                os.remove('%s%s' %(localpath,newfile))
                                return HttpResponse('输入远程的文件路径以"/"结尾哦')
                            if rightpath=='/':
                                sftp.put('%s%s' %(localpath,newfile),'%s%s' %(path,newfile))
                                t.close()
                            else:
                                os.remove('%s%s' %(localpath,newfile))
                                return HttpResponse('你是玩Linux的吗，不知道路径后面需要有"/"啊，赶紧回去加个杠，文件就不需要你指定了！！哈哈')
                        except Exception,e:
                             os.remove('%s%s' %(localpath,newfile))
                             print str(e)
                             return HttpResponse('失败了，请检查代码。。')
                    os.remove('%s%s' %(localpath,newfile))
                    hoststr=hoststr.rstrip(',')
                    applyuser=user_dict['user']
                    models.opdlog.objects.create(contentsorfilename=newfile,approuser_id='1',dealuser_id=1,logtype=models.logtype.objects.get(id=3),applyuser=models.User.objects.get(username=applyuser),hostlist=hoststr)
                    return render_to_response('opd/success/fileuploadsuccess.html')
                else:
                  return HttpResponse('请选择上传的文件，') 
        else:
            uf = UserForm()
            allidc=models.IDC.objects.all()
            return render_to_response('opd/upload.html',{'allidc':allidc,'uf':uf,'allhost':allhost,'username':user_dict['user']})
    else:
        return redirect('/login/')