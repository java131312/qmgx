#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import io
import json
import time
from opd import models
from opd import command
from django.utils import timezone
from datetime import date, datetime
from django.core import serializers
from django.core.context_processors import request
from opd.models import orderstatus
from opd.timeformat import  timeformat
from opd.publicserver.power import powercheck
@powercheck
def logdetail(request):
    user_dict=request.session.get('is_login',None)
    logtype=request.GET.get('logtype')
    if user_dict:
        if logtype=='1':
            alllog=models.opdlog.objects.filter(logtype=1).order_by('-create_at')
            return render_to_response('opd/opdlog/index.html',{'alllog':alllog}) 
        elif logtype=='2':
            #start =datetime.now()
            #abc=datetime(2016,11,1,0,0,0)
            #cba=datetime(2016,11,30,23,59)
            logmonth=models.opdlog.objects.filter(logtype=logtype)
            year_month=set()
            for i in logmonth:
                year_month.add((i.create_at.year,i.create_at.month))
            #print year_month
            counter = {}.fromkeys(year_month,0)
            #print counter
            for i in logmonth:
                counter[(i.create_at.year,i.create_at.month)]+=1
            #print counter
            year_month_number = []
            for key in counter:
                year_month_number.append([key[0],key[1],counter[key]])
            year_month_number.sort(reverse=True)
            #print year_month_number
            #return HttpResponse(json.dumps(year_month_number))
            #logmonth=models.opdlog.objects.filter(logtype=2,create_at__year='2016').order_by('-create_at')
            #logmonth.query.group_by = ['create_at__month']
           # print logmonth
            #november=models.opdlog.objects.filter(logtype=2,create_at__year='2016',create_at__month='11').order_by('-create_at')
            #november=models.opdlog.objects.filter(logtype=2,create_at__range=(abc,cba)).order_by('-create_at')
            #january=models.opdlog.objects.filter(logtype=2,create_at__year='2016',create_at__month='12').order_by('-create_at')
            #return render_to_response('opd/opdlog/configmodlog.html',{'logmonth':logmonth,'alllog':november,'january':january,'username':user_dict['user']}) 
            return render_to_response('opd/opdlog/configmodlog.html',{'logmonth':year_month_number,'username':user_dict['user']}) 
        elif logtype=='3':
            logmonth=models.opdlog.objects.filter(logtype=logtype)
            year_month=set()
            for i in logmonth:
                year_month.add((i.create_at.year,i.create_at.month))
            counter = {}.fromkeys(year_month,0)
            for i in logmonth:
                counter[(i.create_at.year,i.create_at.month)]+=1
            year_month_number = []
            for key in counter:
                year_month_number.append([key[0],key[1],counter[key]])
            year_month_number.sort(reverse=True)
            return render_to_response('opd/opdlog/synclog.html',{'logmonth':year_month_number,'username':user_dict['user']})
        elif logtype=='4':
            logmonth=models.opdlog.objects.filter(logtype=logtype)
            year_month=set()
            for i in logmonth:
                year_month.add((i.create_at.year,i.create_at.month))
            counter = {}.fromkeys(year_month,0)
            for i in logmonth:
                counter[(i.create_at.year,i.create_at.month)]+=1
            year_month_number = []
            for key in counter:
                year_month_number.append([key[0],key[1],counter[key],logtype])
            year_month_number.sort(reverse=True)
            return render_to_response('opd/opdlog/shelllog.html',{'logmonth':year_month_number,'username':user_dict['user']})
        elif logtype=='5':
            logmonth=models.opdlog.objects.filter(logtype=logtype)
            year_month=set()
            for i in logmonth:
                year_month.add((i.create_at.year,i.create_at.month))
            counter = {}.fromkeys(year_month,0)
            for i in logmonth:
                counter[(i.create_at.year,i.create_at.month)]+=1
            year_month_number = []
            for key in counter:
                year_month_number.append([key[0],key[1],counter[key],logtype])
            year_month_number.sort(reverse=True)
            return render_to_response('opd/opdlog/crondlog.html',{'logmonth':year_month_number,'username':user_dict['user']})    
        elif user_dict and request.method=='POST':
            year=request.POST.get('year')
            month=request.POST.get('month')
            logtype=request.POST.get('logtype')
            logresult=models.opdlog.objects.filter(logtype=logtype,create_at__year=year,create_at__month=month).values('applyuser__nickname','hostlist','contentsorfilename','describe','create_at').order_by('-create_at')
            logresult=list(logresult)
            try:
                return HttpResponse(json.dumps(logresult,cls=timeformat.CJsonEncoder))
            except Exception,e:
                print e.message
        else:
            return HttpResponse('对不起，你操作有误。。。')
    else:
         return redirect('/login/') 