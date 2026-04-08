from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), #127.0.0.1:8000/
    path('register/', views.register_view, name='register'), #127.0.0.1:8000/register/
]