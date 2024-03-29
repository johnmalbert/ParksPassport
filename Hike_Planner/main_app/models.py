from django.db import models
import re
import datetime

# Create your models here.
#User Class, First Name, Last Name, Address, Saved Hikes, Completed Hikes
class UserManager(models.Manager):
    def UserValidation(self, postData):
        errors = {}
        if(len(postData['first_name']) < 2) or not postData['first_name'].isalpha():
            errors['first_name'] = "First name must be at least 2 alphabetical characters."
        if(len(postData['last_name']) < 2) or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must be at least 2 alphabetical characters"
        # if(len(postData['password']) < 8) or len(postData['confirm']) < 8:
        #     errors['password'] = "Password must be at least 8 characters"
        # if postData['password'].isalpha():
        #     errors['letters'] = "Password must contain 1 or more numbers or special characters"
        if postData['password'] != postData['confirm']:
            errors['match_pw'] = "Confirmation Password doesn't match."
        if User.objects.filter(email=postData['email'].lower()):
            print("Email is already in db", postData['email'])
            errors['user_exists'] = "Email address is taken."
        if len(postData['zipcode']) != 5:
            errors['zipcode'] = "Zipcode must be 5 digits"        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    zipcode = models.IntegerField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #visited_parks = list of all the parks visited by user
    #park_ratings = list of all the parks rated by user

class Park(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    desc = models.TextField()
    long = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    img_url2 = models.CharField(max_length=255, default="nps.png")
    img_url3 = models.CharField(max_length=255, default="nps.png")
    img_url4 = models.CharField(max_length=255, default="nps.png")
    img1_desc = models.TextField(null = True)
    img2_desc = models.TextField(null = True)
    img3_desc = models.TextField(null = True)
    img4_desc = models.TextField(null = True)
    parkCode = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visits = models.ManyToManyField(User, related_name="visited_parks")
    # rating = models.ManyToManyField(User, related_name="park_rating")

class Rating(models.Model):
    owner = models.ForeignKey(User, related_name="ratings", on_delete = models.CASCADE)
    parkId = models.IntegerField()
    parkRating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
