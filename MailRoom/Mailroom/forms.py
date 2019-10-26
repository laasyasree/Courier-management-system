from django import forms
from django.contrib.auth.models import User
from.import models
class Register(forms.ModelForm):
	class Meta:
		model=models.OtherUsers
		fields=('user','phone','rollNo','Mail_Id')
class Package(forms.ModelForm):
    OTP=forms.CharField(max_length=7,required=False)
    class Meta:
        model=models.Package
        fields=('Number','Company','RollNo','Phone','OTP')
class Retrieve(forms.ModelForm):
    OTP=forms.CharField(max_length=7,label='OTP')
    RollNo=forms.CharField(max_length=30,label='RollNo')
    class Meta:
        model=models.Retrieve
        fields=('OTP','RollNo')
