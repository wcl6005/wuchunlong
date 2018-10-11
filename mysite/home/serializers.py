"""
from rest_framework import serializers 
from api.models import Product 
class ProductSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Product 
        fields = ('id', 'created', 'name', 'describe', 'price', 'isDelete')
"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password','groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

