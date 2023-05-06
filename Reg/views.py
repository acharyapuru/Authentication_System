from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Reg.forms import SignupForm,SigninFrom,PassChangeForm,EditAdminProfileForm,EditUserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def Signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created Successfully!!!')
            return HttpResponseRedirect('signin')
            
    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})
def Signin(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
         form=SigninFrom(request=request,data=request.POST)
         if form.is_valid():
            uname=form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully!!!")
                return HttpResponseRedirect('/profile/')
        else:
            form=SigninFrom()
        return render(request,'signin.html',{'form':form})
    else:
       return HttpResponseRedirect('/profile/')

def Profile(request):
    if request.user.is_authenticated:
     if request.method=='POST':
       if request.user.is_superuser:
        form=EditAdminProfileForm(request.POST,instance=request.user)
        users=User.objects.all()
       else:
         form=EditUserProfileForm(request.POST,instance=request.user)
         users=None
       if form.is_valid():
          form.save()
          messages.success(request,'Profile updated successfully!!!')
     else:
        if request.user.is_superuser:
           form=EditAdminProfileForm(instance=request.user)
           users=User.objects.all()
        else:
           form=EditUserProfileForm(instance=request.user)
           users=None
     return render(request,'profile.html',{'name':request.user,'form':form,'users':users})
    else:
       return HttpResponseRedirect('/signin/')

def Signout(request):
    logout(request)
    messages.success(request,'Logged out successfully!!!')
    return HttpResponseRedirect('/signin/')

def Password_Change(request):
   if request.user.is_authenticated:
      if request.method=='POST':
         form=PassChangeForm(user=request.user,data=request.POST)
         if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully!!!')
            return HttpResponseRedirect('/profile/')
      else:
         form=PassChangeForm(user=request.user)
      return render(request,'passwordchange.html',{'form':form})
   else:
      return HttpResponseRedirect('/signin/')


def Userdeteil(request,id):
   if request.user.is_authenticated:
      if request.user.is_superuser:
         pi=User.objects.get(pk=id)
         if request.method=='POST':
            form=EditAdminProfileForm(user=request.user,instance=pi)
            if form.is_valid():
               form.save()
               messages.success(request,'updated successfully!!!')
         else:
            form=EditAdminProfileForm(instance=pi)
         return render(request,'userdetail.html',{'form':form})
      else:
         return HttpResponseRedirect('/profile/')
   else:
      return HttpResponseRedirect('/signin/')
   