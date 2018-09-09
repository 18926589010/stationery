from django.shortcuts import render, HttpResponse
from django.contrib.auth import  authenticate, login, logout
from account.form import LoginForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def userlogin(request):
    if request.method == "POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            cd=login_form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user:
                login(request,user)
                return HttpResponse('WELCOME')
            else:
                return HttpResponse('Failed')
        else:
            return HttpResponse('invalid login')
    if request.method == "GET":
         login_form= LoginForm()
         return render(request,"login.html",{"form": login_form})

def userlogout(request):
    logout(request)
    context={}
    return render(request, 'logout.html', context)
