from django.urls import path
from . import views

urlpatterns = [
    path('signIn/', views.signIn_User, name='signin'),
    path('getstarted/', views.signUp_User, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('onboard/', views.profile_setup_view, name='onboard'),
    path('signout/', views.signout_user, name='signout')
]
