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
        read_only_fields = ["category_owner"]


class ItemDetailSerializer(ItemSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.store = validated_data.get("store", instance.store)
        instance.link = validated_data.get("link", instance.link)
        instance.image = validated_data.get("image", instance.image)
        instance.ranking = validated_data.get("ranking", instance.ranking)
        instance.favourite = validated_data.get("favourite", instance.favourite)
        instance.purchased = validated_data.get("purchased", instance.purchased)
        instance.cost = validated_data.get("cost", instance.cost)
        instance.comments = validated_data.get("name", instance.comments)
        # HAVEN'T ADDED OTHER USER UPDATES YET
        instance.save()
        return instance


class ListDetailSerializer(ListIndividualSerializer):
    items = ItemSerializer(many=True, read_only=True)
