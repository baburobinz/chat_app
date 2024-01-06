from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import *

def user_login(request):
   data = UserMessages.objects.all()   
   if request.user.is_authenticated:
      return render(request,'home.html',{'data':data})
   elif request.POST:
      user_name = request.POST.get('username')
      password = request.POST.get('password')
     
      user = authenticate(username=user_name,password=password)
      if user is not None:
         login(request,user)
         return render(request,'home.html',{'data':data})

   return render(request,'login.html')

def user_creation(request):
    if request.POST:
      user_name = request.POST.get('username')
      password = request.POST.get('password')
      f_name = request.POST.get('first_name')
      l_name = request.POST.get('last_name')
      try:
        user = User.objects.create_user(username=user_name,first_name=f_name,last_name=l_name,password=password)
        return redirect('user_login')
      except Exception:
         return HttpResponse('user already exist')
    return render(request,'signup.html')

def signout(request):   
   logout(request)
   return redirect('user_login')