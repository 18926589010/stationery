
from django.shortcuts import render, redirect
from stationery.models import stationery, stat_type, purchase,provider,order_record_master,order_record_slave
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, HttpResponse
from deviceman.models import user_list
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
#from api.serializers import StaionerySerializer
import datetime
import json
from django.db.models import F

# Create your views here.

def index(request):

    #stats = stationery.objects.all()
    stats = stationery.objects.values_list('stat_type','stat_type__name').annotate(Count('stat_type'))
    print(stats.query)
    print(stats)
    orders = order_record_master.objects.filter(order_status= 'submitted')
    return render(request,'stationery/stat_index.html', {'stats':stats ,'orders':orders})

def stat_list(request):
    id=request.GET.get('id')
    stat_list=stationery.objects.filter(stat_type=id)
    print(stat_list)
    return render(request,'stationery/stat_list.html',{'stat_list':stat_list })

def order_detail(request):
    orderid=request.GET.get('orderid')
    orders=order_record_slave.objects.filter(order_record_master_id=orderid)
    users=order_record_master.objects.values('user_list_id').filter(id=orderid)


    userid=users[0]['user_list_id']
    users_list=user_list.objects.filter(id=userid)

    return render(request,'stationery/order_detail.html',{'orders':orders, 'users_list': users_list,'orderid': orderid})

@csrf_exempt
def stat_apply_index(request):
    user_list_id=request.session.get('user_list_id')
    full_name=request.session.get('full_name')
    orderid=request.session.get('orderid',42)
    print(orderid)
    if user_list_id==None:
        return HttpResponseRedirect('apply_login')
    #cart = request.session.get("cart", None)
    #carts = order_record_master.objects.filter(user_list_id=user_list_id, order_status='submitted')
    if request.method == 'GET':
        stationerys=order_record_slave.objects.values('stationery__spec').annotate(number=Sum("order_num"),spec=F('stationery__spec'),id=F('stationery_id'), name=F('stationery__name')).order_by('-number')[:10]
        print(stationerys)
        return render(request, 'stationery/stat_apply_index.html', {'stationerys': stationerys})
        #return render(request, 'stationery/stat_apply_index.html', {'carts': carts,'stationerys':stationerys})
    if request.method=='POST':
        stationery_name=request.POST.get('stationery_name')
        stationerys=stationery.objects.filter(name__icontains=stationery_name)
        return render(request, 'stationery/stat_apply_index.html', {'stationerys': stationerys})
        #return render(request,'stationery/stat_apply_index.html',{'carts':carts,'stationerys':stationerys})

def add_to_cart(request):
    user_list_id=request.session.get('user_list_id',None)
    statid=request.GET.get('statid')
    #obj=models.order_record(stationery_id=20,user_list_id=243, num=1)
    order_record_master.objects.create(order_status='submitted',user_list_id=243,date='2018-08-30')
    order_record_slave.objects.create(order_num=1,order_record_master_id=3,stationery_id=12)
    #obj.save()
    #carts=order_record.objects.filter(user_list_id=243)
    #print(carts)
    return HttpResponseRedirect('stat_apply_index')

def clean_cart(request):
    user_list_id=request.session.get('user_list_id')
    orderid=request.session.get('orderid')
    order_record_slave.objects.filter(order_record_master_id=orderid).delete()
    #order_record_master.objects.filter(user_list_id=user_list_id, order_status='shopping').delete()


    return HttpResponseRedirect('stat_apply_index')

def submit_cart(request):
    user_list_id=request.session.get('user_list_id')
    orderid=request.session.get('orderid')
    print(user_list_id)
    print(orderid)
    #orderid=request.session.get('orderid')
    order_record_master.objects.filter(user_list_id=user_list_id, id=orderid).update(order_status='submitted')
    request.session['orderid']=''
    del request.session['user_list_id']
    return HttpResponseRedirect('apply_login')

def complete_order(request):
    orderid=request.GET.get('orderid')
    order_record_master.objects.filter(id=orderid).update(order_status='Completed')
    return HttpResponseRedirect('index')

@csrf_exempt
def apply_login(request):
    if request.method=='GET':
        return render(request,'stationery/apply_login.html')
    if request.method=='POST':

        email_address=request.POST.get('email_address')
        #print(email_address)
        users=user_list.objects.filter(email_address=email_address)
        for user in users:
            #查询是否有未提交的申请，
            request.session['user_list_id'] = user.id  # #把当前user_list_id传给session
            request.session['full_name'] = user.full_name     #把当前full_name传给session
            request.session['email_address']=email_address
            request.session['dept_name'] = user.dept_list.dept_name

            order_record_masters=order_record_master.objects.filter(user_list_id=user.id, order_status='shopping')
            if order_record_masters.exists():
                for order in order_record_masters:
                    request.session['orderid']=order.id   #如果有未提交的申请，取出ID号，传递给session
                    print(order.id)

            else:
                # 如果没有查询到未提交的申请，就创建一条主记录
                order_record_master.objects.create(date=datetime.datetime.now().strftime("%Y-%m-%d"), order_status='shopping',user_list_id=user.id)
                print(user.id)
                orders=order_record_master.objects.filter(user_list_id=user.id, order_status='shopping')
                print(orders)
                for order in orders:
                    request.session['orderid']=order.id
                    print(order.id)
        return HttpResponseRedirect("apply_index")
        #return render(request,'stationery/apply_index.html',{'users':users})



def ajax(request):
    id=request.GET.get('id')
    orderid=request.GET.get('orderid')
    #user_list_id=request.session.get('user_list_id',None)
    msg='sucessfully'
    #print(id)
    #print(msg)
    print("get the stationery id is '%s'"%(id))
    print("get order is is '%s'"%(orderid))
           #search if there is any same stationery_id on the shopping orderid
    res=order_record_slave.objects.filter(order_record_master_id=orderid, stationery_id=id )

    if res.exists():
        print("find same stationery '%s'" % (id))
        for stat in res:
            id = stat.id
            print("stat id is '%s'"%(id))
            obj=order_record_slave.objects.get(id=id)
            obj.order_num=obj.order_num+1
            obj.save()
            stats = order_record_slave.objects.filter(order_record_master_id=orderid).values('stationery__name', 'order_num')
            ret = list(stats)
            result = json.dumps(ret)
            return HttpResponse(result, "application/json")
    else:
        print("not found any same stationery")
        order_record_slave.objects.create(order_num=1, order_record_master_id=orderid, stationery_id=id)
        #stats=serializers.serialize('json',order_record_master.objects.filter(id=orderid))
        stats= order_record_slave.objects.filter(order_record_master_id=orderid).values('stationery__name', 'order_num')
        ret = list(stats)
        result = json.dumps(ret)
        return HttpResponse(result, "application/json")

def apply_index(request):
    return render(request,'stationery/apply_index.html')

