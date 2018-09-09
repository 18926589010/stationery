from django.test import TestCase

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from deviceman.models import user_list, dept_list, pc_list, borrows
from django.db.models import Value

# Create your tests here.

def test_update_user(request):

    user_list.objects.filter(id=1).update(full_name='liutest')
    return HttpResponse('sucessfully')

def get_user_id(request):
    pcs=pc_list.objects.filter(id=6)
    for pc in pcs:
        userid=pc.user_list_id
        user_list.objects.filter(id=userid).update(user_status='Inactive')



    return HttpResponse(userid)