#coding:utf-8
import sys

forks=10

def target_host(hosts):
    target_string = ""
    hosts_string = ""
    for hrow in hosts.split(','):
            hosts_string += hrow.split('*')[0]+";"
    target_string=hosts_string[0:len(hosts_string)-1]
    print target_string
    return target_string