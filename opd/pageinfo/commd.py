#coding:utf-8
def try_int(arg,default):
    #ret=None
    try:
        arg=int(arg)
        if arg==0:
            arg=default
    except Exception,e:
        arg=default
    return arg