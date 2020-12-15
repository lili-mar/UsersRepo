from django.urls import path
from . import views


urlpatterns = [
  
    #localhost:8000
    path('', views.landing),  #GET route renders landing.html.  Login/Reg = localhost:8000
    path('register', views.register),  #POST
    path('login', views.login),     #POST
    path('logout', views.logout),
    
    path('success', views.success),  #This is your new APPLICATION
    
]