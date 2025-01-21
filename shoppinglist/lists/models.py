from django.db import models
from django.contrib.auth import get_user_model


class ListCategory(models.Model):
    category_name = models.CharField(max_length=255)
    category_budget = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category_owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="owned_categories",
    )
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories_modified",
        null=True,
        blank=True,
    )
    archived_at = models.DateTimeField(blank=True, null=True)
    archived_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories_archived",
        null=True,
        blank=True,
    )


class ListIndividual(models.Model):
    list_name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True, null=True)
    individual_budget = models.IntegerField(blank=True, null=True)
    category_id = models.ForeignKey(
        "ListCategory",
        on_delete=models.CASCADE,
        related_name="lists",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    list_owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="owned_lists",
    )
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="lists_modified",
        null=True,
        blank=True,
    )
    archived_at = models.DateTimeField(blank=True, null=True)
    archived_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="lists_archived",
        null=True,
        blank=True,
    )


class Items(models.Model):
    list_id = models.ForeignKey(
        "ListIndividual",
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=255)
    store = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    image = models.URLField(blank=True)
    ranking = models.IntegerField()
    favourite = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    cost = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="owned_items",
    )
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="items_modified",
        null=True,
        blank=True,
    )
    archived_at = models.DateTimeField(blank=True, null=True)
    archived_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="items_archived",
        null=True,
        blank=True,
    )
