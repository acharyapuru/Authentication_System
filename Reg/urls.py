from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Signup,name='signup'),
    path('signin/',views.Signin,name='signin'),
    path('profile/',views.Profile,name='profile'),
    path('signout/',views.Signout,name='signout'),
    path('changepassword/',views.Password_Change,name='changepassword'),
    path('userdetail/<int:id>/',views.Userdeteil,name='userdetail')
    
]
