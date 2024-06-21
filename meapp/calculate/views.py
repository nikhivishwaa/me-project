from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from .heat_gain import TotalHeatLoad
from rest_framework.response import Response
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    print(request.user.username)
    return render(request,'base.html')

    



class HeatCalculationViewSet(ViewSet):

    def create(self, request):
        heat_load = TotalHeatLoad(request.data)

        response = {
            'success': True, 
            'data': {
                    "total_heat_load":str(heat_load), 
                    "air_conditioning": heat_load.tons_of_airconditioning()
                }
        }
        return Response(response, content_type='application/json')

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
                username = email.split('@')[0].replace('.','')
                newuser = User.objects.create_user(username = username, 
                                                    email = email, 
                                                    first_name = firstname,
                                                    last_name = lastname)

                newuser.set_password(password)
                print('User created', newuser)
                newuser.save()
                return redirect('login')

    return render(request, 'login.html', context = {'page':'signup'}) 

    
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
