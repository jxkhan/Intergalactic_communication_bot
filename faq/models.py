from django.db import models
from django.contrib.auth.models import AbstractUser



class Customer(AbstractUser):
    is_guest = models.BooleanField(default=False)


class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
 


    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='faqs')
    keywords = models.JSONField(default=list)
    views = models.IntegerField(default=0)
    helpful_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question