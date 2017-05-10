#coding:utf-8
'''
Created on 2017年2月23日

@author: gty
'''
import time
class datatimestr():
    def __init__(self,timestr):
        self.month=timestr
    @property
    def start(self):
        try:
            if self.month=='01':
                self.month='Jan'
            elif self.month=='02':
                self.month='Feb'
            elif self.month=='03':
                self.month='Mar'
            elif self.month=='04':
                self.month='Apr'
            elif self.month=='05':
                self.month='May '
            elif self.month=='06':
                self.month='Jun '
            elif self.month=='07':
                self.month='Jul'
            elif self.month=='08':
                self.month='Aug'
            elif self.month=='09':
                self.month='Sep'
            elif self.month=='10':
                self.month='Oct'
            elif self.month=='11':
                self.month='Nov'
            else:
                self.month='Dec '
            return self.month
        except Exception,e:
            print e.message
            return 'error'