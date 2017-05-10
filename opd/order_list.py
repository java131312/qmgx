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
from opd.models import orderstatus
def orderapply(request):
    user_dict=request.session.get('is_login',None)
    permission=request.session.get('permission',None)
    ulid=request.GET.get('ulid')
    liid=request.GET.get('liid')
    if user_dict:
        if permission['permi']==1:
            task=models.tasktype.objects.all()
            approval=models.User.objects.all()
            deal=models.User.objects.all()
            orderstatus=models.orderstatus.objects.get(id=1)
            status=orderstatus.taskstatus
            return render_to_response('opd/order_apply.html',{'ulid':ulid,'liid':liid,'task':task,'approval':approval,'deal':deal,'orderstatus':status,'username':user_dict['user']})
        else:
            task=models.tasktype.objects.all()
            approval=models.User.objects.all()
            deal=models.User.objects.all()
            orderstatus=models.orderstatus.objects.get(id=1)
            status=orderstatus.taskstatus
            return render_to_response('opd/order_apply2.html',{'ulid':ulid,'liid':liid,'task':task,'approval':approval,'deal':deal,'orderstatus':status,'username':user_dict['user']})
    else:
        return redirect('/login/')
def tasksubmit(request):
        user_dict=request.session.get('is_login',None)
        permission=request.session.get('permission',None)
        if request.method=='POST' and user_dict:
            if permission['permi']==1:
                try:
                    Title=request.POST.get('regular')
                    Describe=request.POST.get('textarea')
                    applyuser=user_dict['user']
                    task=request.POST.get('tasktype')
                    approval=request.POST.get('approval')
                    deal=request.POST.get('deal')
                    applystatus=2
                    applydate=request.POST.get('applydate')
                    models.orderapply.objects.create(advice='',title=Title,Describe=Describe,applyUser=models.User.objects.get(username=applyuser),task=models.tasktype.objects.get(id=task),approval=models.User.objects.get(id=approval),deal=models.User.objects.get(id=deal),status=models.orderstatus.objects.get(id=applystatus),date=applydate)
                    models.opdlog.objects.create(logtype_id=1,applyuser=models.User.objects.get(username=applyuser),approuser=models.User.objects.get(id=approval),dealuser=models.User.objects.get(id=deal),describe='申请了订单')
                    return render_to_response('opd/success/orderapplysuccess.html',{'username':user_dict['user']})
                except Exception,e:
                    print e.message
                    return HttpResponse('失败了，请检查。。')
            else:
                try:
                    Title=request.POST.get('regular')
                    Describe=request.POST.get('textarea')
                    applyuser=user_dict['user']
                    task=request.POST.get('tasktype')
                    approval=request.POST.get('approval')
                    deal=request.POST.get('deal')
                    applystatus=2
                    applydate=request.POST.get('applydate')
                    models.orderapply.objects.create(advice='',title=Title,Describe=Describe,applyUser=models.User.objects.get(username=applyuser),task=models.tasktype.objects.get(id=task),approval=models.User.objects.get(id=approval),deal=models.User.objects.get(id=deal),status=models.orderstatus.objects.get(id=applystatus),date=applydate)
                    models.opdlog.objects.create(logtype_id=1,applyuser=models.User.objects.get(username=applyuser),approuser=models.User.objects.get(id=approval),dealuser=models.User.objects.get(id=deal),describe='申请了订单')
                    return render_to_response('opd/success/orderapplysuccess2.html',{'username':user_dict['user']})
                except Exception,e:
                    return HttpResponse('失败了，请检查。。')
def orderlist(request):
    user_dict=request.session.get('is_login',None)
    permission=request.session.get('permission',None)
    if user_dict:
        if permission['permi']==1:
            applyuser=user_dict['user']
            applycontent=models.orderapply.objects.filter(applyUser=models.User.objects.get(username=applyuser).id).order_by("status_id")
            userid=models.User.objects.get(username=applyuser).id
            #print models.IDC.objects.last()
            return render_to_response('opd/order_list.html',{'applycontent':applycontent,'username':user_dict['user'],'userid':userid})
        else:
            applyuser=user_dict['user']
            applycontent=models.orderapply.objects.filter(applyUser=models.User.objects.get(username=applyuser).id).order_by("status_id")
            #print models.IDC.objects.last()
            userid=models.User.objects.get(username=applyuser).id
            return render_to_response('opd/order_list2.html',{'applycontent':applycontent,'username':user_dict['user'],'userid':userid})
    else:
        return redirect('/login/')
def modifyapply(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        id=request.GET.get('id')
        approvalid=models.orderapply.objects.get(id=id).approval_id
        dealid=models.orderapply.objects.get(id=id).deal_id
        applyuser=user_dict['user']
        applycontent=models.orderapply.objects.get(applyUser=models.User.objects.get(username=applyuser).id,id=id)
        task=models.tasktype.objects.all()
        deal=models.User.objects.all()
        approval=models.User.objects.all()
        orderstatus=models.orderapply.objects.get(id=id)
        status=orderstatus.status
        return render_to_response('opd/order_modify.html',{'dealid':dealid,'approvalid':approvalid,'id':id,'orderstatus':status,'approval':approval,'task':task,'deal':deal,'applycontent':applycontent,'username':user_dict['user']})
    else:
        return redirect('/login/')
def submitmodifyapply(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        id=request.POST.get('applyid')
        title=request.POST.get('regular')
        Describe=request.POST.get('textarea')
        applyuser=user_dict['user']
        task=request.POST.get('tasktype')
        approval=request.POST.get('approval')
        deal=request.POST.get('deal')
        applydate=request.POST.get('applydate')
        content=models.orderapply.objects.get(id=id)
        content.title= title
        content.Describe=Describe
        content.applyuser_id=applyuser
        content.task_id=task
        content.approval_id=approval
        content.deal_id=deal
        content.date=applydate
        content.status_id=2
        content.save()
        return redirect('/orderlist')
def approvallist(request):
    user_dict=request.session.get('is_login',None)
    permission=request.session.get('permission',None)
    if user_dict:
        if permission['permi']==1:
            username=user_dict['user']
            userid=models.User.objects.get(username=username).id
            approvallist=models.orderapply.objects.filter(approval_id=userid).order_by("status_id")
            return render_to_response('opd/order_approval.html',{'approvallist':approvallist,'username':user_dict['user']})
        else:
            username=user_dict['user']
            userid=models.User.objects.get(username=username).id
            approvallist=models.orderapply.objects.filter(approval_id=userid).order_by("status_id")
            return render_to_response('opd/order_approval2.html',{'approvallist':approvallist,'username':user_dict['user']})
    else:
        return redirect('/login/')
def agreeapp(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        id=request.POST.get('applyid')
        advice=request.POST.get('textarea')
        content=models.orderapply.objects.get(id=id)
        content.advice=advice
        content.status_id=3
        content.save()
        return redirect('/approval/')
def deallist(request):
    user_dict=request.session.get('is_login',None)
    permission=request.session.get('permission',None)
    if user_dict:
        if permission['permi']==1:
            username=user_dict['user']
            userid=models.User.objects.get(username=username).id
            deallist=models.orderapply.objects.filter(deal_id=userid).order_by("status_id")
            return render_to_response('opd/order_deal.html',{'deallist':deallist,'username':user_dict['user']})
        else:
            username=user_dict['user']
            userid=models.User.objects.get(username=username).id
            deallist=models.orderapply.objects.filter(deal_id=userid).order_by("status_id")
            return render_to_response('opd/order_deal2.html',{'deallist':deallist,'username':user_dict['user']})
    else:
        return redirect('/login/')
def appdeal(request):
    user_dict=request.session.get('is_login',None)
    
    if user_dict:
        id=request.POST.get('dealid')
        dealcontent=request.POST.get('textarea')
        content=models.orderapply.objects.get(id=id)
        content.dealcontent=dealcontent
        content.status_id=5
        content.save()
        return redirect('/deal/')
def applyagree(request):
    user_dict=request.session.get('is_login',None)
    id=request.GET.get('id')
    approvalid=request.GET.get('approvalid')
    if request.method=='POST':
        agreeid=request.POST.get('agreeid')
        if agreeid=='3':
            newid=request.POST.get('applyid')
            advice=request.POST.get('textarea2')
            content=models.orderapply.objects.get(id=newid)
            content.advice=advice
            content.status_id=3
            content.save()
            return redirect('/approval')
        else:
            newid=request.POST.get('applyid')
            advice=request.POST.get('textarea2')
            content=models.orderapply.objects.get(id=newid)
            content.advice=advice
            content.status_id=4
            content.save()
            return redirect('/approval/')
    elif user_dict:
        if approvalid=='3':
            approid=models.orderapply.objects.get(id=id).approval_id
            dealid=models.orderapply.objects.get(id=id).deal_id
            userid=models.orderapply.objects.get(id=id).applyUser_id
            applyuser=user_dict['user']
            applycontent=models.orderapply.objects.get(applyUser_id=userid,id=id)
            task=models.tasktype.objects.all()
            deal=models.User.objects.all()
            approval=models.User.objects.all()
            orderstatus=models.orderapply.objects.get(id=id)
            status=orderstatus.status
            return render_to_response('opd/order_agree.html',{'dealid':dealid,'approvalid':approid,'id':id,'orderstatus':status,'approval':approval,'task':task,'deal':deal,'applycontent':applycontent,'username':user_dict['user']})
        elif approvalid=='4':
            approid=models.orderapply.objects.get(id=id).approval_id
            dealid=models.orderapply.objects.get(id=id).deal_id
            userid=models.orderapply.objects.get(id=id).applyUser_id
            applycontent=models.orderapply.objects.get(applyUser_id=userid,id=id)
            task=models.tasktype.objects.all()
            deal=models.User.objects.all()
            approval=models.User.objects.all()
            orderstatus=models.orderapply.objects.get(id=id)
            status=orderstatus.status
            return render_to_response('opd/order_deny.html',{'dealid':dealid,'approvalid':approid,'id':id,'orderstatus':status,'approval':approval,'task':task,'deal':deal,'applycontent':applycontent,'username':user_dict['user']})
    else:
        return redirect('/login/')