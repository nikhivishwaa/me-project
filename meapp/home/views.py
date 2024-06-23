from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .validation.signup import signup_request_validation
from . import validators
from .helper import create_user
import json
import random as rd


@login_required(login_url="/login")
def dashboard(request):
    return render(request,'dashboard.html', context={'walls': range(1,5)})

def register(request):
    if request.method == 'POST':
        
        formdata = signup_request_validation(request)
        if formdata['isvalid']:  
            d = formdata['data']          
            user = User.objects.filter(email=d['email'])
            if user.exists():
                messages.error(request, "User already exist")
                return redirect('signup')

            else:
                username = d['email'].split('@')[0].replace('.','_')
                try:
                    create_user(d, username)
                    messages.success(request, "Account Created. Now you can Login")

                except IntegrityError:
                    username += f'{rd.randint(123,4562) + abs(rd.randint(123,4562) - 1954)}'
                    create_user(d, username)
                    messages.success(request, "Account Created. Now you can Login")
        
                return redirect('signup')
        else:
            return render(request, 'signup.html', context = formdata['data'])

    return render(request, 'signup.html') 

def logoutuser(request):
    logout(request)
    # messages.success(request, 'User has been logged out')
    return redirect('login')

@login_required(login_url="/login")
def profile(request):
    if request.user.is_authenticated:
        user = {
                'username' : request.user.username,
                'email' : request.user.email,
                'firstname' : request.user.first_name,
                'lastname' : request.user.last_name
            }
        return HttpResponse(json.dumps(user), content_type='application/json')

    
def userauth(request):
    if request.user.is_authenticated:
        return redirect('/')

    elif request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        if email and password:
            try:
                username = User.objects.get(email=email).username
                print('username', username)
                user = authenticate(username=username, password=password)
                print('user', user)
                if user is not None:
                    login(request, user)
                    return redirect('/dashboard')

                else:
                    messages.error(request, "Invalid Credentials")
                    return render(request, 'login.html')
                
            except Exception as e:
                messages.error(request, "User not exist")
                return render(request, 'login.html')
        else:
            messages.error(request, f"{'Password' if not password else 'Email'} is missing")
            return render(request, 'login.html')


    return render(request, 'login.html')
