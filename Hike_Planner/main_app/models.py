from django.db import models

# Create your models here.
#User Class, First Name, Last Name, Address, Saved Hikes, Completed Hikes
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#Hike Class....pull from API?