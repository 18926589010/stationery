from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from deviceman.models import user_list, dept_list, pc_list, borrows
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
from datetime import datetime
from deviceman.form import UserModelForm, PcModelForm, borrowsModelForm
from django.http import HttpResponseRedirect


def testdb(request):
    user1=user_list(user_name='liuzh',full_name='Liu, Zhehao', email_address='zhehao.liu@aecom.com',dept_no='dept03')
    user1.save()
    return HttpResponse('user数据添加成功！')

def t_dept_list(request):
    dept1=dept_list(dept_id='dept22',dept_name='test',dept_leader='liuhonghai')
    dept1.save()
    return HttpResponse('dept数据添加成功！')

@csrf_exempt
def get_user(request):

    id=request.POST.get('id',)
    if id=='':
        print('Null')
    else:
        #users=user_list.objects.filter(id=id)
        users = user_list.objects.filter(dept_list__dept_name__icontains=id,)
        return render(request,'hello.html',{'users':users,'i':10, 'id':id})
       # return HttpResponse(users)

@csrf_exempt
def display_user(request):
    users={}
    userid=request.POST.get('userid',)
    userstatus=request.POST.get('user_status')
    if userid==None:
        userid='xxx'
    if userstatus == None:
        users = user_list.objects.filter(Q(user_name__icontains=userid)|Q(full_name__icontains=userid)|Q(dept_list__dept_name__icontains=userid)|Q(email_address__icontains=userid))
    else:
        users = user_list.objects.filter((Q(user_name__icontains=userid) | Q(full_name__icontains=userid) | Q(
            dept_list__dept_name__icontains=userid) | Q(email_address__icontains=userid))&Q(user_status=userstatus))
    return render(request,'display_user.html',{'users':users, 'id':userid})

@csrf_exempt
def display_pc(request):
    pcs={}
    if request.method == 'GET':
        id=request.GET.get('pcid')

        pcs = pc_list.objects.filter( id=id )

        return render(request, 'display_pc.html', {'pcs': pcs, 'id': id})
    else:
         pcid=request.POST.get('pcid',)
    if pcid==None:
        pcid='cnshz1pcxxx'

    pcs = pc_list.objects.filter(Q(host_name__icontains=pcid)|Q(service_tag__icontains=pcid)|Q(user_list__full_name__icontains=pcid))
   # print(users)
    return render(request,'display_pc.html',{'pcs':pcs, 'id':pcid})

@csrf_exempt
def update_user_status(id, u_status):
    user_list.objects.filter(id=id).update(user_status=u_status)

def update_user_resigndate(id):
    user_list.objects.filter(id=id).update(resigndate=str(datetime.now().date()))

@csrf_exempt
def update_pc(request):


    id=request.GET.get('id',)
    request.session['search_pc_key']=id
    #id=7
    action=request.GET.get('action',)
    pcs=pc_list.objects.filter(id=id)
    for pc in pcs:
        full_name=pc.user_list.full_name
        userid=pc.user_list_id
        #return HttpResponse(userid)


    if action=='collect':
        pcs = pc_list.objects.filter(id=id).update(user_list_id='180', host_status='inventory', seat_no='14000',\
                                                   remark=Concat('remark', Value('['+full_name+' 收回日期'+str(datetime.now().date())+']')))
    elif action=='dispose':
        pcs = pc_list.objects.filter(id=id).update(user_list_id='193', host_status='P-Dispose', seat_no='14000',\
                                                   remark=Concat('remark', Value('['+full_name+' 申请报废'+str(datetime.now().date())+']')))
    else:
        update_user_status(userid, 'Inactive')
        update_user_resigndate(userid)
        #user_list.objects.filter(id=userid).update(resigndate=str(datetime.now().date()), user_status='Inactive')
        pcs=pc_list.objects.filter(id=id).update(user_list_id='180', host_status='inventory',remark=Concat('remark', Value('['+full_name+' 离职日期'+str(datetime.now().date())+']')))
    pcs = pc_list.objects.filter(id=id)
        #return HttpResponse(userid)
    return render(request,'display_pc.html',{'pcs':pcs, 'id': id })

@csrf_exempt
def get_username_from_pcid(pcid):
    #pcid = request.GET.get('id', )
    pclist= pc_list.objects.filter(id=pcid)
    for pcs in pclist:
        userid=pcs.user_list_id
        userlist = user_list.objects.filter(id=userid)
        for users in userlist:
            username = users.full_name
    return username

def newdevice(request):
    context={}
    context['pcid']=request.GET.get('pcid')
    request.session['ifnew'] = 'Yes'
    return render(request, 'newdevice.html', context,)

@csrf_exempt
def adddevice(request):

    ifnew=request.session.get('ifnew',default='No')
    host_name= request.POST.get('host_name',)
    if host_name==None:
        host_name='NO DATA'
    service_tag = request.POST.get('service_tag',)
    host_type = request.POST.get('host_type',)
    host_model = request.POST.get('host_model',)
    host_spec = request.POST.get('host_spec',)
    price = request.POST.get('price', )
    receive_date=request.POST.get('datepicker')
    full_name=request.POST.get('full_name')
    seat_no=request.POST.get('seat_no')
    host_status=request.POST.get('host_status')
    studio = request.POST.get('studio')
    location= request.POST.get('location')
    asset_code=request.POST.get('asset_code')
    remark=request.POST.get('remark')
    context={}
    context['host_name']=host_name
    context['service_tag']=service_tag
    context['host_type']=host_type
    context['host_model'] = host_model
    context['host_spec']=host_spec
    context['price'] = price
    context['receive_date'] = receive_date
    context['full_name'] = full_name
    context['seat_no']=seat_no
    context['host_status'] = host_status
    context['studio'] = studio
    context['location'] = location
    context['asset_code'] = asset_code
    context['remark'] = remark
    context['ifnew']=ifnew
    result=pc_list.object.filter(host_name=host_name)
    pcs=pc_list(host_name=host_name,service_tag=service_tag, host_type=host_type, host_model=host_model, host_spec=host_spec,\
                price=price, receive_date=receive_date, user_list_id=180, seat_no=seat_no, host_status=host_status, studio=studio, \
                location='CNSHZ1',asset_code=1,remark=remark )
    pcs.save()
    return render(request,'newdevice.html',context)

def usercreate(request):
    if request.method == "GET":
        obj = UserModelForm()
        return render(request, "usercreate.html", {'obj': obj})
    elif request.method == "POST":
        obj = UserModelForm(request.POST)
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
            save_status="用户信息已经成功创建"
        else:
            print(obj.errors.as_json())
            save_status='出错，请检查你输入的信息'
        return render(request, "usercreate.html", {'obj': obj,'status':save_status})

@csrf_exempt
def useredit(request):
        #request.method == "GET":
    userid=request.GET.get('userid')
    userobj=user_list.objects.get(id=userid)
    if request.method == 'POST':
        obj = UserModelForm(request.POST, instance=userobj)
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
            return HttpResponseRedirect('display_user.html?userid='+userid)
        else:
            print(obj.errors.as_json())
    obj=UserModelForm(instance=userobj)
    return render(request, "useredit.html", {'obj': obj, 'userid': userid})





@csrf_exempt
def pccreate(request):
    if request.method == "GET":
        obj = PcModelForm()
        return render(request, "newdevice.html", {'obj': obj, 'acton': 'pccreate', 'modelname': '-新建设备'})
    elif request.method == "POST":
        obj = PcModelForm(request.POST)
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
        else:
            print(obj.errors.as_json())
    return render(request, "newdevice.html", {'obj': obj, 'acton': 'pccreate', 'modelname': '-新建设备'})

@csrf_exempt
def pcedit(request):

    pcid = request.GET.get('pcid')
    if pcid != None:
        pcobj = pc_list.objects.get(id=pcid)
    if request.method == 'POST':
        obj = PcModelForm(request.POST, instance=pcobj)  #
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
            return HttpResponseRedirect('display_pc?pcid='+pcid)
        else:
            print(obj.errors.as_json())
    obj = PcModelForm(instance=pcobj)
    return render(request, "newdevice.html", {'obj': obj, 'acton': 'pcedit', 'modelname': '-编辑设备'})

@csrf_exempt
def borrowscreate(request):
    if request.method == "GET":
        obj = borrowsModelForm()
        return render(request, "borrowpc.html", {'obj': obj, 'acton': 'borrowscreate', 'modelname': '-新建设备'})
    elif request.method == "POST":
        obj = borrowsModelForm(request.POST)
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
        else:
            print(obj.errors.as_json())
    return render(request, "borrowpc.html", {'obj': obj, 'acton': 'borrowscreate', 'modelname': '-新建设备'})

def borrowsedit(request):
    pcid = request.GET.get('pcid')
    if pcid != None:
        bobj = borrows.objects.get(Q(pc_list_id=pcid)&Q(rdate__isnull = True))
        #obj = borrowsModelForm(instance=bobj)
    #bid = request.GET.get('bid')
    #if bid != None:
        #obj = borrows.objects.get(id=pcid)
    #else:
        #return HttpResponseRedirect('')
    if request.method == 'POST':
        obj = borrowsModelForm(request.POST, instance=bobj)  #
        print(obj.is_valid())  # 这是方法，别忘记了加括号
        print(obj.cleaned_data)
        print(obj.errors)
        if obj.is_valid():
            obj.save()
            #return HttpResponseRedirect('deviceman')
        else:
            print(obj.errors.as_json())
    obj = borrowsModelForm(instance=bobj)
    return render(request, "borrowpc.html", {'obj': obj, 'acton': 'borrowsedit','pcid':pcid, 'modelname': '-编辑设备'})

def report(request):
    context={}
    return render(request, 'report.html',context)

@csrf_exempt
def planmap(request):
    if request.method=="GET":
        seatno=request.GET.get("seatno")
        pcs=pc_list.objects.filter(seat_no=seatno)
        return render(request,"map.html",{'pcs': pcs,'seatno':seatno})
    else:
        if request.method=='POST':
            seatno=request.POST.get("seatno")
            pcs={}
            pcs = pc_list.objects.filter(seat_no=seatno)
            #return render(request, "map.html", {'pcs': pcs, 'seatno': seatno})
    return render(request, "map.html", {'pcs': pcs, 'seatno': seatno})

@csrf_exempt
def gps(request):
    seatno = request.GET['seatno']
    #pcs = pc_list.objects.filter(seat_no=seatno)
    return HttpResponse(seatno)