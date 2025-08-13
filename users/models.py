from django.db import models
import uuid
# Create your models here.

class User (models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20,blank=True,null=True)
    profile_img = models.ImageField(upload_to="profile/",blank=True,null=True)
    preferences = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'

    def __str__(self):
        return self.name
