#coding:utf-8
import ConfigParser
import codecs
class Configget(object):
    def default(self):
        config=ConfigParser.ConfigParser()
        with codecs.open(r'./qmgx/opd/config.conf','r+',encoding='utf-8') as cfgfile:
            config.readfp(cfgfile)
        localpath=config.get("global","getlocalpath")
        return localpath
    def upload(self):
        config=ConfigParser.ConfigParser()
        with codecs.open(r'./qmgx/opd/config.conf','r+',encoding='utf-8') as cfgfile:
            config.readfp(cfgfile)
        localpath=config.get("global","uploadlocalpath")
        return localpath