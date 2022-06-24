from django.urls import path
from django.conf.urls import url
from Bidwars import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('editpro',views.editpro,name='editpro'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('error', views.error, name='error'),  
    path('add', views.add, name='add'),
    path('search', views.search, name='search'), 
    path('preview', views.preview, name='preview'),
    path('pricing', views.pricing, name='pricing'), 
    path('product', views.product, name = 'product'),
    path('emails', views.emails, name = 'emails'),
    path('confirm', views.confirm, name = 'confirm'),
]