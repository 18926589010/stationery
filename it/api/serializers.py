from django.contrib.auth.models import User, Group
from rest_framework import serializers
from stationery.models import stationery

class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class StaionerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = stationery
        fields = ('stationery','order_num')
