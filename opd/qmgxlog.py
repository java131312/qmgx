#coding:utf-8
import redis
import os
import sys
import signal
import  subprocess
import  time
import random
def monitorLog(logfile):
	r = redis.Redis(host='192.168.0.185',port=6379,db=0)
        stoptime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 10))
        popen = subprocess.Popen('tail -f ' + logfile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid = popen.pid
        print('Popen.pid:' + str(pid))
        while True:
            line = popen.stdout.readline().strip()+'\n'
	    print (line)
            # 判断内容是否为空
            if line:
		nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
		math=random.randint(0,99999999)
		keyvalue='%s%s' %(nowtime,math)
	#	print keyvalue
		r.lpush('log',line)
		#return line
            # 当前时间
            thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
           # if thistime >= stoptime:
                # 终止子进程
            #    popen.kill()
             #   print '杀死subprocess'
              #  break
if __name__ == '__main__':
    #monitorLog('/usr/local/nginx/logs/django.log')
    monitorLog(sys.argv[1])
