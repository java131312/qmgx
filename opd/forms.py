#coding:utf-8
from django import forms
class UserForm(forms.Form):
    headImg = forms.FileField(label='选择文件')
    #subject = forms.CharField(max_length=100 ,label='留言标题')