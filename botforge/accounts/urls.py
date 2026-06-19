from django.urls import path
from .views import (register_view,login_view,dashboard,logout_view,company_setup,get_profile_details)

urlpatterns = [
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path("setup/",company_setup,name="company_setup"),
    path("profile-details/",get_profile_details,name="get_profile_details"),
]