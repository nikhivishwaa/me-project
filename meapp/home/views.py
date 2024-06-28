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
    return render(request,'home/home.html')

def about(request):
    return render(request,'home/about.html')

def contact(request):
    return render(request,'home/contact.html')

@login_required(login_url="/login")
def calculate(request):
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

    return render(request,'home/calculator.html', context={'walls_iter': range(1,5), 'rights': rights})
