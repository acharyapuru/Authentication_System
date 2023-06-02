from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Signin),
    path('signup/',views.Signup,name='signup'),
    path('signin/',views.Signin,name='signin'),
    path('profile/',views.Profile,name='profile'),
    path('signout/',views.Signout,name='signout'),
    path('changepassword/',views.Password_Change,name='changepassword'),
    path('userdetail/<int:id>/',views.Userdeteil,name='userdetail'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('password_reset_request/',views.password_reset_request,name='password_reset_request'),
    path('password_reset/<uidb64>/<token>',views.password_reset_confirm,name='password_reset'),
    
]
