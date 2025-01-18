from django.db import models
from django.contrib.auth import get_user_model

class ListCategory(models.Model):
    category_budget = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    category_name = models.CharField(max_length=255, blank=True)
    archived_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='category_owner_modifier' 
    )
    archived_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='category_owner_archiver' 
    )
    created_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='category_owner_creator' 
    )

class ListIndividual(models.Model):
    individual_budget = models.IntegerField(blank=True, null=True)
    archived_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True, null=True)
    category_id = models.ForeignKey(
       'ListCategory',
       on_delete=models.CASCADE,
       related_name='list_category' 
    )
    list_owner = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner' 
    )
    modified_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_modifier' 
    )
    archived_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_archiver' 
    )
    created_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_creator' 
    )
    