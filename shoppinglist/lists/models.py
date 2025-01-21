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
        null=True,
        blank=True,
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
