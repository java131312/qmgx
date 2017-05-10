from __future__ import absolute_import
from celery import shared_task
import socket
from opd import models
from opd.serverinstall import installcmd
from opd.serverinstall import checknrpe
from django.db import transaction
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from django.db.models.query import QuerySet
import sys
import time
from opd import cmd
import datetime
from opd.datestrftime import timestrf 
@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    print 'hh'
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
@shared_task
def install_aliveness(hostbox,allserver):
    servername=models.serverinstall.objects.get(id=allserver)
    servername=servername.installservername
    try:
        for item in hostbox:
            hostServer=models.Server.objects.get(id=item)
            username=hostServer.account
            password=hostServer.passwd
            serveripaddr=hostServer.ipaddrs
            hostname=hostServer.hostname
            item=[item]
            Runobj=installcmd.Installserver([serveripaddr],username,password,servername,hostname)
            abc=Runobj.ansible_playbook()
            item=''.join(item)
            if abc[serveripaddr]['unreachable']>=1 or abc[serveripaddr]['failures']>=1:
                flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=item),servername=models.serverinstall.objects.get(id=allserver))
                flushstatus.installstatus_id=4
                flushstatus.save()
            #print abc[serveripaddr]['failures']
            #if abc[item][unreachable]==1:
             #   pass
            else:
                flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=item),servername=models.serverinstall.objects.get(id=allserver))
                flushstatus.installstatus_id=1
                flushstatus.save()
        return 'OK'
    except Exception,e:
        for item in hostbox:
            flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=item),servername=models.serverinstall.objects.get(id=allserver))   
            if flushstatus.installstatus_id==3:
                flushstatus.installstatus_id=4
                flushstatus.save()
        return 'faild'
@shared_task
def check_aliveness(servername):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    if servername==1:
        nrpeserver=models.Hostinstalldetail.objects.filter(servername__installservername='nrpe',installstatus_id=1)
        for item in nrpeserver:
            nrpeserverid=item.hostmachine_id
            nrpeserverip=models.Server.objects.get(id=nrpeserverid).ipaddrs
            flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=nrpeserverid),servername_id=1)
            #checknrpe.check_aliveness(nrpeserverip, 5666)
            checknrperesult.delay(nrpeserverip,5666,nrpeserverid,1)
            '''
            try:
                sk.connect((nrpeserverip,5666))
                #sys.exit(1)
            except socket.gaierror,e:
                print "Address-related error connecting to server: %s" % e
                #sys.exit(1)
            except socket.error, e:
                print "Connection error: %s" % e
                flushstatus.installstatus_id='2'
                flushstatus.save()
        sk.close()        #sys.exit(1)
        '''
        return 'success nrpe check'
@shared_task
def check_failaliveness(servername):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    if servername==1:
        nrpeserver=models.Hostinstalldetail.objects.filter(servername__installservername='nrpe',installstatus_id=2)
        for item in nrpeserver:
            nrpeserverid=item.hostmachine_id
            nrpeserverip=models.Server.objects.get(id=nrpeserverid).ipaddrs
            flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=nrpeserverid),servername_id=1)
            checknrperesult.delay(nrpeserverip,5666,nrpeserverid,2)
        return 'check nrpe master'
        '''
            try:
                sk.connect((nrpeserverip,5666))
                flushstatus.installstatus_id='1'
                flushstatus.save()
                #sys.exit(1)
            except socket.gaierror,e:
                print "Address-related error connecting to server: %s" % e
            #continue
                #sys.exit(1)
            except socket.error, e:
                print "Connection error: %s" % e
            finally:
                print 'jixu'
                #sys.exit(1)
        sk.close()
        return 'fail nrpe check'      
            #print 'server %s %d service is OK!' %(ip,port)
        #except Exception,e:
            #print 'server %s %d service is NOT OK!'  %(ip,port)
        '''
@shared_task()
def checknrperesult(ip, port,nrpeserverid,type):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    if type==2:
        try:
            sk.connect((ip,port))
            sk.close()
            flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=nrpeserverid),servername_id=1)
            flushstatus.installstatus_id='1'
            flushstatus.save()
                #sys.exit(1)
        except socket.gaierror,e:
            print "Address-related error connecting to server: %s" % e
            #sys.exit(1)
        except socket.error, e:
            print "Connection error: %s" % e
                #sys.exit(1)
        return 'fail nrpe check'
    else:
        try:
            sk.connect((ip,port))
            sk.close()
                #sys.exit(1)
        except socket.gaierror,e:
            print "Address-related error connecting to server: %s" % e
            #sys.exit(1)
        except socket.error, e:
            flushstatus=models.Hostinstalldetail.objects.get(hostmachine=models.Server.objects.get(id=nrpeserverid),servername_id=1)
            flushstatus.installstatus_id='2'
            flushstatus.save()
            print "Connection error: %s" % e
                #sys.exit(1)
        return 'nrpe check'
@shared_task()
def Crtnumber():
    allproject=models.Project.objects.all()
    '''
    hour=time.strftime("%H")
    year=time.strftime("%Y")
    day=time.strftime("%d")
    month=time.strftime("%m")
    '''
    now=datetime.datetime.now()
    delta=datetime.timedelta(hours=-1)
    n_days=now+delta
    now=now.strftime('%d/%m/%Y:%H:00:00')
    lastmonth=now.split('/')[1]
    lastmonth=timestrf.datatimestr(lastmonth)
    lastmonth=lastmonth.start
    lastdays=now.split('/')[0]
    lastyears=now.split('/')[2]
    
    n_days=n_days.strftime('%d/%m/%Y:%H:00:00')
    prevmonth=n_days.split('/')[1]
    prevmonth=timestrf.datatimestr(prevmonth)
    prevmonth=prevmonth.start
    prevdays=n_days.split('/')[0]
    prevyears=n_days.split('/')[2]
    for i in allproject:
        if i.project=='QMGX':
            shellcmd='''awk '$4>"[%s/%s/%s"&&$4<"[%s/%s/%s"' /usr/local/nginx/logs/quanmingexing_server.log|wc -l''' %(prevdays,prevmonth,prevyears,lastdays,lastmonth,lastyears)
            hostObj=cmd.client('192.168.0.10','root','qmgx@123',shellcmd,'nginx')
            hostObj=hostObj.logcountnumber
            if hostObj=='error':
                models.Crtnumber.objects.create(number='0',projectclass_id='1')
            else:
                models.Crtnumber.objects.create(number=hostObj,projectclass_id='1')
            '''
            filemonth=timestrf.datatimestr(month)
            filemonth=filemonth.start
            print filemonth
            dbmonth=models.Crtnumber.objects.all().order_by("-create_at")[0]
            dbmonth=dbmonth.create_at
            resultdbmonth=str(dbmonth).split('-')[1]
            resuultdbmonth=timestrf.datatimestr(resultdbmonth)
            resuultdbmonth=resuultdbmonth.start
            print resuultdbmonth
            resultdbyear=str(dbmonth).split('-')[0]
            print year
            print resultdbyear
            if filemonth==resuultdbmonth and year==resultdbyear:
                if hour=='00':
                    shellcmd=''awk '$4>"[23/Feb/2017:10:00:00"&&$4<"[23/Feb/2017:11:00:00"' /usr/local/nginx/logs/access.log|wc -l''
                    print 'cuowu'
                else:
                    prevhour=int(hour)-1
                    shellcmd=''awk '$4>"[%s/%s/%s:%s:00:00"&&$4<"[%s/%s/%s:%s:00:00"' /usr/local/nginx/logs/quanmingexing_server.log|wc -l'' %(day,filemonth,year,prevhour,day,filemonth,year,hour)
                    hostObj=cmd.client('192.168.0.10','root','qmgx@123',shellcmd,'nginx')
                    hostObj=hostObj.logcountnumber
                    models.Crtnumber.objects.create(nubmer=hostObj,projectclass_id='1')
            else:
                print 'wokao'
            #hostObj=cmd.client('192.168.0.10','root','qmgx@123','',service)
            '''
        elif i.project=='QMSS':
            shellcmd='''awk '$4>"[%s/%s/%s"&&$4<"[%s/%s/%s"' /usr/local/nginx/logs/qmss_server.log|wc -l''' %(prevdays,prevmonth,prevyears,lastdays,lastmonth,lastyears)
            hostObj=cmd.client('192.168.0.10','root','qmgx@123',shellcmd,'nginx')
            hostObj=hostObj.logcountnumber
            if hostObj=='error':
                models.Crtnumber.objects.create(number='0',projectclass_id='2')
            else:
                models.Crtnumber.objects.create(number=hostObj,projectclass_id='2')
            '''
            filemonth=timestrf.datatimestr(month)
            filemonth=filemonth.start
            print filemonth
            dbmonth=models.Crtnumber.objects.all().order_by("-create_at")[0]
            dbmonth=dbmonth.create_at
            resultdbmonth=str(dbmonth).split('-')[1]
            resuultdbmonth=timestrf.datatimestr(resultdbmonth)
            resuultdbmonth=resuultdbmonth.start
            print resuultdbmonth
            resultdbyear=str(dbmonth).split('-')[0]
            print year
            print resultdbyear
            if filemonth==resuultdbmonth and year==resultdbyear:
                if hour=='00':
                    shellcmd=''awk '$4>"[23/Feb/2017:10:00:00"&&$4<"[23/Feb/2017:11:00:00"' /usr/local/nginx/logs/access.log|wc -l''
                    print 'cuowu'
                else:
                    prevhour=int(hour)-1
                    shellcmd=''awk '$4>"[%s/%s/%s:%s:00:00"&&$4<"[%s/%s/%s:%s:00:00"' /usr/local/nginx/logs/qmss_server.log|wc -l'' %(day,filemonth,year,prevhour,day,filemonth,year,hour)
                    hostObj=cmd.client('192.168.0.10','root','qmgx@123',shellcmd,'nginx')
                    hostObj=hostObj.logcountnumber
                    models.Crtnumber.objects.create(nubmer=hostObj,projectclass_id='2')
            else:
                print 'wokao'
            #hostObj=cmd.client('192.168.0.10','root','qmgx@123','',service)
            '''
    return 'ok'
