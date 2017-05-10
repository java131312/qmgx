#coding:utf-8
import datetime
from datetime import date
from django.shortcuts import render
from django.shortcuts import render_to_response,HttpResponse,redirect
# Create your views here.
#from bbsapp.extensions import html
import json
class CJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            #return obj.strftime('%Y-%m-%d %H:%M:%S')
            return obj.strftime('%d日 %H:%M:%S')
            print obj
        elif isinstance(obj,date):
            return obj.strftime("%Y-%m-%d")
            print obj
        else:
            return json.JSONEncoder.default(self,obj)
            print obj