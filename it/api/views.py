#from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializers, GroupSerializer

# Create your views here.

class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class Groupviewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

