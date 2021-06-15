from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('upload',views.upload, name='upload'),
    path('home/upload',views.uploadi, name='uploadi'),
    path('details',views.details, name='details'),
    path('home/details',views.detailsi, name='detailsi'),
]