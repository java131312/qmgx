#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse,redirect
import paramiko
import os
import json
import models
from opd import command
from django.utils import timezone
from datetime import date, datetime
from django.core import serializers
from django.core.context_processors import request
from macpath import split
from opd import cmd
from django.conf import settings
from django.core.cache import cache
import redis
'''
Created on 2016年11月18日

@author: gty
'''
# Create your views here.
def prinlog(request):
    user_dict=request.session.get('is_login',None)
    if user_dict:
        allhost=models.Server.objects.all()
        return render_to_response('opd/prinlog.html',{'allhost':allhost,'username':user_dict['user']})
    else:
        return redirect('/')
def tailresult(request):
    ret={'data':''}
    r = redis.Redis(host='192.168.0.7',port=6380,db=0)
    value=r.lrange('log',0,25)
    ret['data']=value
    return HttpResponse(json.dumps(ret))
'''
def tailresult(request):
    #r = redis.Redis(host='192.168.0.7',port=6380,db=0)
    #value=r.get('201611181454242016111814542462269067');
    key='201611181454242016111814542481731582'
    try:
        aaaa = cache.set('wocao','123',settings.NEVER_REDIS_TIMEOUT)
        aaaa = cache.get('201611181538522016111815385226520321')
    
    #print value
        print aaaa
    except Exception,e:
        print e.message
'''        