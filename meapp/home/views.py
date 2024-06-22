from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json
from . import validators

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print(request.user.username)
    return render(request,'home.html', context={'walls': range(1,5)})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')

        if email and password and firstname:
            user = User.objects.filter(email=email)
            print(user)
            if user:
                return redirect('login')

            else:
                if not validators.validate_email(email):
                    return HttpResponse('invalid email')
                username = email.split('@')[0].replace('.','')
                newuser = User.objects.create_user(username = username, 
                                                    email = email, 
                                                    first_name = firstname.strip(), 
                                                    last_name = lastname.strip())

                newuser.set_password(password)
                print('User created', newuser)
                newuser.save()
                return redirect('login')

    return render(request, 'login.html', context = {'page':'signup'}) 

def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

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
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            if email and password:
                username = email.split('@')[0].replace('.','')
                user = authenticate(username=username, password=password)
                print('user', user)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                
        except Exception as e:
            return redirect('login')


    return render(request, 'login.html', context = {'page':'login'})
