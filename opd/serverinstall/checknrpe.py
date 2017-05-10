#coding:utf-8
import socket
def check_aliveness(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect(('192.168.0.88',22))
        print ip,port
        print 'server %s %d service is OK!' %(ip,port)
        return 'aaaa'
    except Exception,e:
        print e.message
        print ip,port
        print type(ip)
        print 'server %s %d service is NOT OK!'  %(ip,port)
        return 'hh'
    finally:
        sk.close()
    return 'ddd'