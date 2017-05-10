#coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from opd.ansible import cronttab
from opd.Crtnumber import crtnumber
from opd.serverinstall import serverinstall
from opd.jenkins import jenkinsapi
urlpatterns = patterns('',
                     url(r'^cronttab/', cronttab.cronttab), 
                     url(r'^cronlist/',cronttab.cronlist),
                     url(r'^crondel/',cronttab.crondel),
                     url(r'install/',serverinstall.serverinstall),
                     url(r'serverdetail/',serverinstall.serverdetail),
                     url(r'serveropd/',serverinstall.serveropd),
                     url(r'getinstalldis/',serverinstall.getinstalldis),
                     url(r'modcrontab/',cronttab.modcrontab),
                     url(r'getcrontime/',cronttab.getcrontabtime),
                     url(r'getnumber/',crtnumber.crtnumber),
                     url(r'jenkinsproject/',jenkinsapi.getproject)
            )