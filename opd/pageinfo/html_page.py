#coding:utf-8
from django.utils.safestring import mark_safe
class PageInfo:
    def __init__(self,current_page,all_count,per_item=5):
        self.CurrentPage=current_page
        self.AllCount=all_count
        self.PerItem=per_item
    @property
    def start(self):
        return (self.CurrentPage-1)*self.PerItem
    @property
    def end(self):
        return self.CurrentPage*self.PerItem
    @property
    def all_page_count(self):
      
        all_page=divmod(self.AllCount,self.PerItem)
        if all_page[1]==0:
            all_page_count=all_page[0]
        else:
            all_page_count=all_page[0]+1
        return all_page_count
def Pager(page,all_page_count):
    '''
    page：当前页
    all_page_count:总页数
    '''
    
    page_html=[]
    first_html="<div class='col-md-5'> <ul class='pagination'><li><a href='/list/1'>first</a></li>"
    last_html="<li><a href='/list/%d'>last</a></li></ul><div>" %(all_page_count)
    page_html.append(first_html)
  
    if page<=1:
        prev_html="<li class='disabled'><a href='javascript:void(0);'>&larr; Prev</a></li>"
    else:
        prev_html="<li><a href='/list/%d'>&larr; Prev</a></li>"%(page-1,)
    page_html.append(prev_html)
    begin=page-3
    end=page+2
    #没有显示11页
    if all_page_count<6:
        begin=0
        end=all_page_count
    else:
        if page<3:
            begin=0
            end=5
        else:
            if page+3>all_page_count:
                begin=page-3
                end=all_page_count
            else:
                begin=page-3
                end=page+2
    for i in range(begin,end):
        if page==i+1:
            a_html="<li class='active'><a  href='/list/%d'>%d</a></li>"%(i+1,i+1)
        else:
            a_html="<li><a  href='/list/%d'>%d</a></li>"%(i+1,i+1)
        page_html.append(a_html)
    #page=mark_safe("<a href='/index2/1'>1</a>")
    if page>=all_page_count:
        next_html="<li class='disabled'><a href='javascript:void(0);'>Next &rarr;</a></li>"
    else:
        next_html="<li><a href='/list/%d'>Next &rarr;</a></li>"%(page+1,)
    page_html.append(next_html)
    #end_html="<a href='/list/%d'>尾页</a>"%(all_page_count)
    page_html.append(last_html)
    page=mark_safe(' '.join(page_html))
    return page