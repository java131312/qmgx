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
def crtnumber(request):
    now=datetime.datetime.now()
    delta=datetime.timedelta(hours=-12)
    n_days=now+delta
    n_days=n_days.strftime('%Y-%m-%d %H:%M:%S')
    qmgxallnumber=models.Crtnumber.objects.filter(projectclass='1',create_at__gte=n_days)
    qmgxlist=[]
    qmgxlist1=[]
    for i in qmgxallnumber:
        qmgxlist.append(int(i.number))
        newdate=str(i.create_at).split()[1]
        newdate=str(newdate).split(':')[0]
        qmgxlist1.append(newdate)
    #qmgxallnumber=list(qmgxallnumber)
    #qmgxalldate.append(qmgxallnumber)
    qmssallnumber=models.Crtnumber.objects.filter(projectclass='2',create_at__gte=n_days)
    qmsslist=[]
    qmsslist1=[]
    for i in qmssallnumber:
        qmsslist.append(int(i.number))
        newdate=str(i.create_at).split()[1]
        newdate=str(newdate).split(':')[0]
        qmsslist1.append(newdate)
    resultlist=[qmgxlist1,qmgxlist,qmsslist]
    return HttpResponse(json.dumps(resultlist,cls=timeformat.CJsonEncoder))
    