#coding:utf-8
from opd import models
from django.shortcuts import render,render_to_response,HttpResponse,redirect
from functools import wraps
def powercheck(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        user_dict=request.session.get('is_login',None)
        if user_dict:
            role=models.User.objects.get(username=user_dict['user']).user_type_id
            if role==1:
                return func(request,*args,**kwargs)
            else:
                return HttpResponse('你无权访问')
        else:
            return redirect('/login/')
        #return func(request,*args,**kwargs)
    return wrapper