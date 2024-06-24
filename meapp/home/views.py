from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="/login")
def dashboard(request):
    return render(request,'home/dashboard.html')

def landingpage(request):
    return render(request,'home/index.html')

@login_required(login_url="/login")
def calculate(request):
    return render(request,'home/calculator.html', context={'walls': range(1,5)})

