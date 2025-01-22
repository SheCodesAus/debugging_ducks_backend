from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User


class ListIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('lists.ListIndividual')
        fields = '__all__'


class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('lists.ListCategory')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class CustomAuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()

