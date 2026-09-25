from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expences(models.Model):
    title = models.CharField(max_length=100)
    
    CATEGORY_OPTIONS=[
        ('food','food'),
        ('Rent','Rent'),
        ('Travel','Travel'),
        ('Groceries','Groceries'),
        ('Fuel','Fuel'),
        ('shopping','shopping'),
        ('billing','billing'),
        ('medical','medical'),
        ('education','education'),
        ('entertainment','entertainment'),
        ('investment','investment'),
        ('Other','Other'),
    ]
    category = models.CharField(max_length=100,choices=CATEGORY_OPTIONS)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.FloatField()
    def __str__(self):
        return self.name
