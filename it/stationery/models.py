from django.db import models
from deviceman.models import user_list
from django.contrib import auth

# Create your models here.

class stat_type(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class stationery(models.Model):
    name = models.CharField(max_length=40)
    spec = models.CharField(max_length=40, default='--')
    stock_num =  models.IntegerField()
    stat_type = models.ForeignKey('stat_type', to_field='id', related_name='stat_type_name', on_delete=False)

    def __str__(self):
        return self.name

class order_record_main(models.Model):
    user_list = models.ForeignKey('deviceman.user_list',on_delete=False)
    date = models.DateField()
    order_status = models.CharField(max_length=40)

class order_record_subordinate(models.Model):
    order_record_main = models.ForeignKey('order_record_main',on_delete=False)
    stationery = models.ForeignKey('stationery',on_delete=False)
    order_num = models.IntegerField()


class purchase(models.Model):
    stationery = models.ForeignKey('stationery', on_delete=False)
    num = models.IntegerField()
    date = models.DateField()
    provider = models.ForeignKey('provider', on_delete=False)
    user = models.ForeignKey('auth.user',on_delete=False, default=1)

class provider(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=40)
    telephone = models.IntegerField()
    email = models.EmailField(max_length=40)
    def __str__(self):
        return self.name

class cart(models.Model):
    user_list = models.ForeignKey('deviceman.user_list', on_delete=False)
    stationery = models.ForeignKey('stationery',on_delete=False)
    num = models.ImageField()