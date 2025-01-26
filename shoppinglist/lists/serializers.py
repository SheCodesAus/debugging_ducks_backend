from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User



class ItemSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.id")

    class Meta:
        model = apps.get_model("lists.Item")
        fields = "__all__"


class ListIndividualSerializer(serializers.ModelSerializer):
    list_owner = serializers.ReadOnlyField(source="list_owner.id")

    class Meta:
        model = apps.get_model("lists.ListIndividual")
        fields = "__all__"



class ListCategorySerializer(serializers.ModelSerializer):
    category_owner = serializers.ReadOnlyField(source="category_owner.id")

    class Meta:
        model = apps.get_model("lists.ListCategory")
        fields = "__all__"
        read_only_fields = ['category_owner']
