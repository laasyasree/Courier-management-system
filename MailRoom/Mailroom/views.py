import smtplib, ssl
import math, random
from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
from . import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import RedirectView
def generateOTP():
    string = '0123456789'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
    return OTP

def sendMail(receiver_email, OTP):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "subhash.prince001@gmail.com"
    password = 'subhash17'
    message = """\
    Subject: Collect Package

    Your package has arrived at the Amrita Mailroom
    Your OTP to collect the package is """ + OTP +'.'+"""

    Regards
    The Mailroom Team."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def sendMailWelcome(receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "subhash.prince001@gmail.com"
    password = 'subhash17'
    message = """\
    Subject: Amrita Mailroom Service Registration Confirmation

    Thank You for registering with our Mailroom Service. Collect your packages when you
    get a notification mail with an OTP from us by verifying the OTP at the Mailroom.

    Regards
    The Mailroom Team.
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def sendRetreivalconf(receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "subhash.prince001@gmail.com"
    password = 'subhash17'
    message = """\
    Subject: Amrita Mailroom Service Registration Confirmation

    This mail is to inform you that your package has been handed over to you.

    Regards
    The Mailroom Team.
    """

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
def signup(request):
    if request.method == 'POST':
        form = forms.Register(request.POST)
        if form.is_valid():
            form.save()
            sendMailWelcome(form.cleaned_data.get('Mail_Id'))
            return redirect('/Mailroom/UserSave/')
        else:
            return render(request, 'Mailroom/signup.html', {'form': form})
    else:
        form = forms.Register()
    return render(request, 'Mailroom/signup.html', {'form': form})

def Package_entry(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = forms.Package(request.POST)
            if form.is_valid():
                generated = generateOTP()
                form.instance.OTP=generated
                form.save()
                User_data = models.OtherUsers.objects.all()
                DataToCheck = form.cleaned_data.get('RollNo')
                for number in User_data:
                    if DataToCheck == number.rollNo:
                        sendMail(number.Mail_Id, generated)
                return redirect('/Mailroom/Packageentry/')
            else:
                return render(request, 'Mailroom/entry.html', {'form': form})
        else:
            form=forms.Package()
        return render(request, 'Mailroom/entry.html', {'form': form})
    else:
        return HttpResponse("Please Signup to access records")
def login(request):
    if request.user.is_authenticated:
        return HttpResponse("you are already logged in")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,
             password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/Mailroom/Home/')
            else:
                return render(request, 'Mailroom/login.html', {'err': 'Wrong credentials provided'})
        else:
            return render(request, 'Mailroom/login.html', {'err': ''})

def logout_view(request):
    logout(request)
    return redirect('/Mailroom/Adminlogout/')

def retrieve(request):
    if request.user.is_authenticated:
        form = forms.Retrieve(request.POST)
        if request.method=='POST':
            if form.is_valid():
                OTP=form.cleaned_data.get('OTP')
                RollNo=form.cleaned_data.get('RollNo')
                roll=models.Package.objects.all()
                mail=models.OtherUsers.objects.filter(rollNo=RollNo)
                Flag=True
                for number in roll:
                    if RollNo==number.RollNo:
                        Flag=False
                        if OTP== number.OTP:
                            if number.Status==False:
                                number.Status=True
                                sendRetreivalconf(mail[0].Mail_Id)
                                print(number.Status)
                                number.save()
                                return redirect('/Mailroom/verified/')
                            else:
                                return HttpResponse("Already Collected")
                        else:
                            return HttpResponse("Wrong OTP")
                if Flag:
                    return HttpResponse("please enter the right Roll Number")
        else:
            return render(request,'Mailroom/delivery.html',{'form':form})
    return render(request,'Mailroom/delivery.html',{'form':form})
def Home(request):
	if request.user.is_authenticated:
		Packages = models.Package.objects.all()
		return render(request, 'Mailroom/home.html',{'Packages':Packages})
	else:
		return HttpResponse("you need to login to access Packages")
def package(request,pk):
    if request.user.is_authenticated:
        Package=models.Package.objects.get(pk=pk)
        return render(request, 'Mailroom/package.html',{'Package':Package})
    else:
        return Httpresponse("You need to login to access these Packages")
