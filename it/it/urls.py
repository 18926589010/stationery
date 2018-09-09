"""it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path

from rest_framework import routers
from api import views, serializers
#from stationery import views

router = routers.SimpleRouter()

router.register('users', views.Userviewset)
router.register('groups', views.Groupviewset)
#router.register('stationery',views.StaionerySerializer)

urlpatterns = [

    path('pi-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('deviceman/', include('deviceman.urls')),
    path('account/', include('account.urls' )),
    path('stationery/', include('stationery.urls' )),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

]
