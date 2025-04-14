from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="/login")
def dashboard(request):
    return render(request,'home/dashboard.html')

def landingpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,'home/dashboard.html')

def about(request):
    return render(request,'home/about.html')

def contact(request):
    return render(request,'home/contact.html')

@login_required(login_url="/login")
def profile(request):
    user = {
            'email' : request.user.email,
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'verified' : request.user.verified,
            'phone_number' : request.user.phone_number,
        }
    return render(request, 'home/profile.html', context=user)

@login_required(login_url="/login")
def calculate(request):
    print("access",request.user.calc_access)
    if request.user.calc_access:
        rights_count = 0
        rights_list = [ 'walls', 'windows', 'roof', 'occupants', 'equipments'] 
        rights = {}

        for right in rights_list:
            rights[right] = request.user.calc_access.__getattribute__(right)
            rights_count += rights[right]

        print(rights, rights_count)

        if not rights_count:
            messages.error(request, 'You are not allowed to access calculator')
            return redirect('/dashboard')

        # return render(request,'home/calculator.html', context={'walls_iter': range(1,5), 'rights': rights})
        return render(request,'home/calc.html', context={'walls_iter': range(1,5), 'rights': rights})

    else:
        messages.error(request, 'You are not authorized to access this calculator')
        return redirect('/dashboard')
