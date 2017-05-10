#coding:utf-8
from django.db import connection
sql="select * from opd_idc"
cursor=connection.cursor()
cursor.execute(sql)
domain_and_record_db_datas=cursor.fetchall()
print type(domain_and_record_db_datas)
print domain_and_record_db_datas
for i in domain_and_record_db_datas:
    print i[0]
    print i[1]
