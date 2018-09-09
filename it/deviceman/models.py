from django.db import models


# Create your models here.

class borrows(models.Model):
    user_list=models.ForeignKey('user_list', to_field='id', on_delete=None)
    pc_list=models.ForeignKey('pc_list',  on_delete=None, to_field='id', default=1)
    bdate=models.DateField(auto_now=True)
    rdate = models.DateField(null=True,blank=True,default='0000-00-00')
    ticketid=models.CharField(max_length=40,null=True,blank=True)

class user_list(models.Model):
    user_name=models.CharField(unique=True, max_length=40, verbose_name='用户名')
    full_name=models.CharField(unique=True, max_length=40)
    email_address=models.CharField(max_length=40)
    dept_list=models.ForeignKey('dept_list', on_delete=None, to_field='id')
    regdate=models.DateField(null=True)
    resigndate=models.DateField(null=True)
    user_status=models.CharField(max_length=40)
    class Meta:
        ordering = ('full_name',)

    def __str__(self):
         return self.full_name

class pc_list(models.Model):
    host_name=models.CharField(max_length=64, unique=True)
    service_tag=models.CharField(max_length=45,unique=True)
    hosttype=models.ForeignKey('hosttype', to_field='id', related_name='hosttype_name', verbose_name='host_type', on_delete=None)
    host_model=models.CharField(max_length=45)
    host_spec=models.CharField(max_length=60)
    price=models.FloatField(default=0)
    receive_date=models.DateField(auto_now_add =False, default='2018-01-01')
    user_list = models.ForeignKey('user_list', to_field='id', related_name='user_list_full_name', on_delete=None, )
    seat_no = models.IntegerField(default=14000)
    host_status=models.CharField(max_length=45)
    studio = models.CharField(max_length=45, default='-')
    site=models.ForeignKey('site',to_field='id', related_name='site_name', on_delete=None)
    asset_code = models.IntegerField(default=1)
    remark=models.TextField(max_length=100, default='-')
    class Meta:
        ordering = ('hosttype','host_name',)

    def __str__(self):
        return self.host_name

class dept_list(models.Model):
    dept_id = models.CharField(max_length=45,unique=True)
    dept_name = models.CharField(max_length=45)
    dept_leader = models.CharField(max_length=45)
    def __str__(self):
        return self.dept_name

class hosttype(models.Model):
    name=models.CharField(max_length=20,unique=True)
    cname=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class site(models.Model):
    sitename=models.CharField(max_length=20, unique=True)
    address=models.CharField(max_length=50)
    def __str__(self):
        return self.sitename




