from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm


class SignupForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email']
        labels={
            'email':'Email',
        
            }
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class SigninFrom(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget=forms.TextInput(attrs={'class':'form-control'})
        self.fields['password'].widget=forms.PasswordInput(attrs={'class':'form-control'})
    
class PassChangeForm(PasswordChangeForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['old_password'].widget=forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password1'].widget=forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password2'].widget=forms.PasswordInput(attrs={'class':'form-control'})

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','date_joined','last_login']
        labels={
            'email':'Email'
        }
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'date_joined':forms.DateTimeInput(attrs={'class':'form-control'}),
            'last_login':forms.DateTimeInput(attrs={'class':'form-control'})
        }
class EditAdminProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields='__all__'
        