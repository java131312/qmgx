#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import md5
import io
import json
from opd import models
from opd import command
from django.utils import timezone
import datetime
import time
from opd.timeformat import  timeformat
from django.core import serializers
from django.core.context_processors import request
from django.db import transaction
from opd.publicserver.power import powercheck
@powercheck
def getproject(request):
    user_dict=request.session.get('is_login',None)
    if request.method=='GET':
        allproject=models.Projenkins.objects.all()
        return render_to_response('opd/jenkins/project.html',{'allproject':allproject,'username':user_dict['user']})
    elif request.method=='POST':
        projectname=request.POST.get('projectname')
        projectaddress=request.POST.get('projectaddress')
        newproject=models.Projenkins.objects.create(project=projectname,projecturl=projectaddress)
        return HttpResponse('非法操作')
    else:
        return HttpResponse('非法操作')
