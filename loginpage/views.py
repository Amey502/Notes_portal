from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=username, password=pwd)


        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, please try again!")

    return render(request, 'loginpage/login_page.html')

def register_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        pwda = request.POST.get('pwda')

        if len(username)==0:
            messages.error(request, "Please enter a valid username!")
            return render(request, 'loginpage/register_page.html')

        if pwd!=pwda:
            messages.error(request, "Passwords do not match!")
            return render(request, 'loginpage/register_page.html')
        
        
        if len(pwd)<8:
            messages.error(request, "Password is weak. Miniumum 8 characters!")
            return render(request, 'loginpage/register_page.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'loginpage/register_page.html')
        
        messages.success(request, "Account created! Please login.")
        User.objects.create_user(username=username, password=pwd)
        return redirect('login')
    
    return render(request, 'loginpage/register_page.html')