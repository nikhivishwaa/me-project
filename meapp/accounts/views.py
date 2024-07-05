from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
import datetime as dt
import random as rd
from .models import CalculatorAccessRole
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import io


User = get_user_model()

from accounts.helpers.validations import SignupDataValidation, ProfileUpdateDataValidation, PasswordUpdateDataValidation
from accounts.helpers.utils import otp_helper, forgot_otp_helper
import json


def register(request):
    if request.method == 'POST':
        dataval = SignupDataValidation(request.POST)
        if dataval.is_valid():  
            d = dataval.data          
            user = User.objects.filter(email = d['email'], phone_number = d['phone_number'])
            if user.exists():
                messages.error(request, "User already exist")
                return redirect('signup')

            else:
                user = User.objects.create_user(**d)
                user.set_password(dataval.password)
                user.save()
                # print('registered successfully', user)
                otp_helper(user)
                messages.success(request, "Account Created")
                messages.success(request, "We have sent an OTP to your email for verification")
        
                return render(request, 'accounts/verifyemail.html', context={'email':user.email, "sent":True})
        else:
            messages.error(request, d.errors)
            return render(request, 'accounts/signup.html', context = dataval.data)

    return render(request, 'accounts/signup.html') 


def verifyemail(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        otp = request.POST.get('otp', '')
        resend = request.POST.get('resend', '')

        if email:
            user = User.objects.filter(email = email)
            if user.exists():
                user = user.first()
                if resend == 'resend':
                    otp_helper(user)
                    messages.info(request, "OTP has been resent successfully")
                    return render(request, 'accounts/verifyemail.html', context={'email':user.email, 'status': 'rensend'})
                
                elif (dt.datetime.now(dt.timezone.utc) - user.otp_timestamp).seconds >= 600:
                    user.email_otp = ''
                    user.save()
                    messages.error(request, "OTP Expired")
                    return render(request, 'accounts/verifyemail.html', context={'email':email, 'status': 'expired'})

                elif user.email_otp == otp:
                    user.verified = True
                    user.email_otp = ''
                    user.calc_access = CalculatorAccessRole.objects.filter(walls = True, 
                                                                           windows = True, 
                                                                           roof = True, 
                                                                           occupants = True, 
                                                                           equipments = True).first()
                    user.save()
                    messages.success(request, "Email Verified")
                    return redirect('login')
                else:
                    messages.error(request, "Invalid OTP")
                    return render(request, 'accounts/verifyemail.html', context={'email':email})
        else:
            messages.error(request, f"{'OTP' if not otp else 'Email'} is missing")
            messages.warning(request, "Login to Continue Verification Process")
            return redirect('login')
    elif request.user.is_authenticated and not request.user.verified:
        if (dt.datetime.now(dt.timezone.utc) - request.user.otp_timestamp).seconds >= 600:
            otp_helper(request.user)
            messages.success(request, "OTP has been sent Successfully")
        
        else:
            remaining = 600 - (dt.datetime.now(dt.timezone.utc) - request.user.otp_timestamp).seconds
            messages.warning(request, f"Wait {round(remaining/60)} more minutes {remaining%60} seconds for new OTP")
            return render(request, 'accounts/verifyemail.html', context={'email':request.user.email})

    return redirect('login')


def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/login")
@csrf_exempt
def profile(request):
    response = {'success': True}
    if request.method == 'POST':
        stream = io.BytesIO(request.body)               
        data = JSONParser().parse(stream)
        profile = ProfileUpdateDataValidation(data)
        if profile.is_valid():  
            d = profile.data          
            user = request.user
            print(dir(user))
            for key, value in d.items():
                user.__setattr__(key,value)

            user.save()
            print('updated successfully', user)
        
            response = {
                'success':True,
                'message': "Profile Updated Successfully",
                'data':{
                    'email' : user.email,
                    'first_name' : user.first_name,
                    'last_name' : user.last_name,
                    'verified' : user.verified,
                    'phone_number' : user.phone_number
                }
        }
        else:
            response['success'] = False
            response['message'] = profile.errors
    else:
        response['data'] = {
            'email' : request.user.email,
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'verified' : request.user.verified,
            'phone_number' : request.user.phone_number,
        }

    return HttpResponse(json.dumps(response), content_type='application/json')
    
def userauth(request):
    if request.user.is_authenticated:
        return redirect('/')

    elif request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        if email and password:
            user = authenticate(email=email, password=password)
            # print('user', user, 'logged in')
            if user is not None:
                login(request, user)
                if user.verified:
                    return redirect('/dashboard')
                else:
                    return redirect('verifyemail')

            else:
                messages.error(request, "Invalid Credentials")
                return redirect('login')
        else:
            messages.error(request, f"{'Password' if not password else 'Email'} is missing")
            return render(request, 'accounts/login.html')


    return render(request, 'accounts/login.html')

def forgotpasswordotp(request):        
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        otp = request.POST.get('otp', '')
        resend = request.POST.get('resend', '')

        if email:
            user = User.objects.filter(email = email)
            if user.exists():
                user = user.first()
                remaining = 0
                fresh = True
                if user.forgot_otp_timestamp is not None:
                    remaining = 600 - (dt.datetime.now(dt.timezone.utc) - user.forgot_otp_timestamp).seconds
                    fresh = False
                if resend == 'resend':
                    if remaining > 0 and user.forgot_password_otp:
                        messages.warning(request, f"Wait {round(remaining/60)} more minutes {remaining%60} seconds for new OTP")
                    else:
                        forgot_otp_helper(user)
                        messages.info(request, f"OTP has been {'resent' if user.forgot_password_otp else 'sent'} successfully")
                    return render(request, 'accounts/forgotpassword.html', context={'email':user.email})
                
                elif remaining <= 0:
                    user.forgot_password_otp = ''
                    user.save()
                    messages.error(request, "OTP Expired")
                    return render(request, 'accounts/forgotpassword.html', context={'email':email})

                elif user.forgot_password_otp == otp:
                    p_token = f'${user.id}_TS_{dt.datetime.now().timestamp()/rd.randint(111, 5964)}${hex(int(user.phone_number))}' 
                    user.password_update_token = p_token
                    user.forgot_password_otp = ''
                    user.forgot_otp_timestamp = None
                    user.save()
                    messages.success(request, "OTP Verified. Now create new password")

                    response = redirect('newpassword')
                    response.set_cookie('p_token', user.password_update_token, max_age=600)
                    return response
                else:
                    messages.error(request, "Invalid OTP")
                    return render(request, 'accounts/forgotpassword.html', context={'email':email})
            else:
                messages.error(request, "Invalid User Email")
                return redirect('forgotpassword')
        else:
            messages.error(request, f"{'OTP' if not otp else 'Email'} is missing")
            return redirect('forgotpassword')

    return render(request, 'accounts/forgotpassword.html', context={'status': 'resend'})

def newpassword(request):
    p_token = request.COOKIES.get('p_token', None)
    print(request.COOKIES)
    print(p_token)
    if p_token is not None:
        if request.method == 'POST':
            dataval = PasswordUpdateDataValidation(request.POST)
            if dataval.is_valid():  
                d = dataval.data          
                user = User.objects.filter(password_update_token = p_token)
                if user.exists():
                    user = user.first()
                    user.set_password(dataval.password)
                    user.save()
                    messages.success(request, "Password Changed Successfully")

                    response = redirect('login')
                    response.set_cookie('p_token', '', max_age=0)
                    return response

                else:
                    messages.error(request, "User not exist")           
                    return render(request, 'accounts/newpassword.html')
            else:
                messages.error(request, dataval.errors)
                return render(request, 'accounts/newpassword.html')

        else:
            return render(request, 'accounts/newpassword.html')

    else:   
        messages.warning(request, "Maximum Time Exceeded. Try again.")
        return redirect('forgotpassword')