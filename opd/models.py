#coding:utf-8
from django.db import models
from django.db.models.fields import CharField
# Create your models here.
class IDC(models.Model):
    housename=models.CharField(u'机房名',max_length=64)
    #Group=models.ManyToManyField('Idcgroup')
    class Meta:
        verbose_name='机房'
        verbose_name_plural='机房'
    def __unicode__(self):
        return '%s' %(self.housename) 
class Idcgroup(models.Model):
    groupname=models.CharField(u'组名',max_length=64)
    Group=models.ManyToManyField('IDC',related_name='hostgroup')
    class Meta:
        verbose_name='分组'
        verbose_name_plural='分组'
    def __unicode__(self):
        return '%s' %(self.groupname)
class Server(models.Model):
    house=models.ForeignKey('IDC')
    status=models.ForeignKey('Serverstatus',default=1)
    hostname=models.CharField(u'主机名',max_length=64)
    ipaddrs=models.IPAddressField(u'ip地址',blank=True)
    account=models.CharField(u'用户名',max_length=64)
    passwd=models.CharField(u'密码',max_length=64)
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    update_at=models.DateTimeField(blank=True)
    servergroup=models.ForeignKey('Idcgroup')
    class Meta:
        verbose_name='服务器'
        verbose_name_plural='服务器'
       # index_together=["house"]
        #列表中的字段将建立索引
    def __unicode__(self):
        return '%s' %(self.hostname) 
class Serverstatus(models.Model):
    content=models.CharField(u'描述',max_length=10)
    class Meta:
        verbose_name='状态'
        verbose_name_plural='状态'
    def __unicode__(self):
        return '%s' %(self.content)
class Fileupload(models.Model):
   
    headImg = models.FileField(upload_to = './qmgx/opd/upload/')
class UserType(models.Model):
    display=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '用户类型表'
    def __unicode__(self):
        return self.display
class User(models.Model):
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    nickname=models.CharField(max_length=50,null=True)
    user_type=models.ForeignKey("UserType")
    class Meta:
        verbose_name_plural = '管理员表'
    def __unicode__(self):
        return self.nickname
class tasktype(models.Model):
    tasktype=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '工单类型'
    def __unicode__(self):
        return self.tasktype
class orderstatus(models.Model):
    taskstatus=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '工单状态'
    def __unicode__(self):
        return self.taskstatus
class orderapply(models.Model):
    title=models.CharField(max_length=50)
    Describe=models.TextField()
    applyUser=models.ForeignKey('User',related_name='appuser')
    task=models.ForeignKey('tasktype')
    approval=models.ForeignKey("User")
    deal=models.ForeignKey("User",related_name='deal')
    status=models.ForeignKey('orderstatus')
    date=models.CharField(max_length=50)
    advice=models.TextField(null=True)
    dealcontent=models.TextField(null=True,default='还未处理，请确认是否审批或联系相关工作人员，谢谢...')
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    update_at=models.DateTimeField(blank=True,auto_now=True)
    class Meta:
        verbose_name_plural = '工单申请列表'
    def __unicode__(self):
        return self.title
class logtype(models.Model):
    type=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '日志类型'
    def __unicode__(self):
        return self.type
class opdlog(models.Model):
    logtype=models.ForeignKey('logtype')
    applyuser=models.ForeignKey('User')
    approuser=models.ForeignKey('User',related_name='approuser',null=True)
    dealuser=models.ForeignKey('User',related_name='dealuser',null=True)
    hostlist=models.TextField(null=True)
    contentsorfilename=models.TextField(null=True)
    describe=models.TextField(null=True)
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    class Meta:
        verbose_name_plural = '运维工单系统日志'
    #def __unicode__(self):
        #return self.applyuser,self.approuser,self.dealuser
class crontab(models.Model):
    server=models.ForeignKey('Server')
    cronname=models.CharField(max_length=50)
    crontime=models.CharField(max_length=128)
    croncontent=models.CharField(max_length=128)
    crondis=models.TextField(null=True)
    cronuser=models.ForeignKey('User')
    deltype=models.IntegerField(max_length=11)
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    update_at=models.DateTimeField(blank=True,auto_now=True)
    class Meta:
        verbose_name_plural = '运维定时任务系统'
    def __unicode__(self):
        return self.cronname
class serverinstall(models.Model):
    installservername=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '安装服务'
    def __unicode__(self):
        return self.installservername
class Hostserver(models.Model):
    servername=models.ForeignKey('Server',related_name='installresult')
    installhost=models.ManyToManyField('serverinstall')
    class Meta:
        verbose_name_plural = '服务器安装'
class Hoststatus(models.Model):
    hoststatus=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '主机服务状态'
    def __unicode__(self):
        return self.hoststatus
class Hostinstalldetail(models.Model):
    hostmachine=models.ForeignKey('Server')
    servername=models.ForeignKey('serverinstall',related_name='detailinstall')
    installdis=models.TextField(null=True)
    installuser=models.ForeignKey('User')
    installstatus=models.ForeignKey('Hoststatus')
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    update_at=models.DateTimeField(blank=True,auto_now=True)
    class Meta:
        verbose_name_plural = '服务器安装详情'
    def __unicode__(self):
        return self.installdis
class Commandcontrol(models.Model):
    command=models.CharField(max_length=50)
    role=models.ForeignKey('UserType')
    class Meta:
        verbose_name_plural = '命令执行控制'
    def __unicode__(self):
        return self.command
class Project(models.Model):
    project=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = '项目管理'
    def __unicode__(self):
        return self.project
class Crtnumber(models.Model):
    number=models.CharField(max_length=50)
    projectclass=models.ForeignKey('Project')
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    class Meta:
        verbose_name_plural = '项目点击率'
    def __unicode__(self):
        return self.number
class Projenkins(models.Model):
    project=models.CharField(max_length=50)
    projecturl=models.CharField(max_length=50)
    lastversion=models.CharField(max_length=50,null=True)
    update_at=models.DateTimeField(blank=True,auto_now=True)
    create_at=models.DateTimeField(blank=True,auto_now_add=True)
    class Meta:
        verbose_name_plural = 'jenkins项目部署'
    def __unicode__(self):
        return self.project