from django.db import models
from django.contrib.auth.models import User
class OtherUsers(models.Model):
    user = models.CharField(max_length=50,blank=False)
    phone = models.IntegerField(blank=False)
    rollNo=models.CharField(max_length=40,blank=False)
    Mail_Id = models.CharField(max_length=200, blank=False )

    def __str__(self):
        return self.user
class Package(models.Model):
    Number=models.IntegerField(blank=False)
    Company=models.CharField(max_length=50,blank=False)
    RollNo=models.CharField(max_length=30,blank=False)
    Phone=models.IntegerField(max_length=12,blank=False)
    OTP=models.CharField(max_length=7,blank=True)
    Status=models.BooleanField(default=False)
    def __str__(self):
        return self.RollNo
class Retrieve(models.Model):
    OTP=models.CharField(max_length=7)
    RollNo=models.CharField(max_length=30)
    def __str__(self):
        return self.RollNo
