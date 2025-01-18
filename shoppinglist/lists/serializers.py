from rest_framework import serializers
from django.apps import apps

class ListIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('lists.ListIndividual')
        fields = '__all__'

