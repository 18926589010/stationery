from . import views
from django.urls import path
urlpatterns = [

    path('login', views.userlogin),
    path('logout', views.userlogout),
]