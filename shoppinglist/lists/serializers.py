from rest_framework import serializers
from django.apps import apps


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("lists.Item")
        fields = "__all__"


class ListIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("lists.ListIndividual")
        fields = "__all__"


class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("lists.ListCategory")
        fields = "__all__"
