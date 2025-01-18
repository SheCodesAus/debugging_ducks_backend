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
       related_name='category_owner_modifier',
       null=True,
       blank=True  
    )
    archived_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='category_owner_archiver',
       null=True,
       blank=True  
    )
    created_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='category_owner_creator',
       null=True,
       blank=True  
    )

class ListIndividual(models.Model):
    list_name = models.CharField(max_length=255, null=True)
    individual_budget = models.IntegerField(blank=True, null=True)
    archived_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True, null=True)
    category_id = models.ForeignKey(
       'ListCategory',
       on_delete=models.CASCADE,
       related_name='list_category',
       null=True,
       blank=True 
    )
    list_owner = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_id',
       null=True,
       blank=True  
    )
    modified_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_modifier',
       null=True,
       blank=True  
    )
    archived_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_archiver',
       null=True,
       blank=True  
    )
    created_by = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='list_owner_creator',
       null=True,
       blank=True  
    )
    