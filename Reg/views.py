from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Reg.forms import SignupForm,SigninFrom,PassChangeForm,EditAdminProfileForm,EditUserProfileForm,PasswordForgotForm,CustomSetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm


def Signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            mail_subject='Activate Your Account'
            message=render_to_string(
               'acc_activate_email.html',{
                  'user':user,
                  'domain':current_site.domain,
                  'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                  'token':account_activation_token.make_token(user)

               }
            )
            to_email=form.cleaned_data['email']
            email=EmailMessage(
               mail_subject,message,to=[to_email]
            )
            email.send()
            messages.success(request,'Account Created Successfully. Please confirm your email address to activate account')
            return HttpResponseRedirect('/signin/')
            
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
   

def activate(request,uidb64,token):
   try:
      uid=force_str(urlsafe_base64_decode(uidb64))
      user=User.objects.get(pk=uid)
   except(TypeError,ValueError,OverflowError,User.DoesNotExist):
      user=None
   if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Your account is activated!!!")
        return HttpResponseRedirect('/signin/')
   else:
      return HttpResponse("Activation link is invalid")
      

def password_reset_request(request):
   if request.method=='POST':
      form=PasswordForgotForm(request.POST)
      if form.is_valid():
         username=form.cleaned_data['username']
         user=User.objects.filter(username=username).first()
         if user is not None:
            subject="Password Reset Request"
            current_site=get_current_site(request)
            message=render_to_string('password_reset_email.html',
            {
               'user':user,
               'domain':current_site,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),
               'token':account_activation_token.make_token(user)
            }
            )
            to_email=user.email
            email=EmailMessage(
               subject,message,to=[to_email]
            )
            email.send()
            messages.success(request, 'Please check your email for instructions on how to reset your password.')
            return HttpResponseRedirect('/signin/')
         else:
            messages.error(request,'User with this username doesnt exist')
            return HttpResponseRedirect('/signin/')
   else:
      form=PasswordForgotForm()
   return render(request,'password_reset_request.html',{'form':form})
            
def password_reset_confirm(request,uidb64,token):
   try:
      uid=force_str(urlsafe_base64_decode(uidb64))
      user=User.objects.get(pk=uid)
   except(TypeError,OverflowError,ValueError,User.DoesNotExist):
      user=None
   if user is not None and account_activation_token.check_token(user,token):
      if request.method=="POST":
         form=CustomSetPasswordForm(user,request.POST)
         if form.is_valid():
            form.save()
            messages.success(request,"Your password has been reset")
            return HttpResponseRedirect('/signin/')
      else:
         form=CustomSetPasswordForm(user)
      return render(request,'password_reset_confirm.html',{'form':form})
   else:
      messages.error(request,"Invalid link")
      return HttpResponseRedirect('/signin/')