from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def insurance(request):
    insurances = Insurance.objects.all()
    return render(request, 'insurance.html', {'insurances': insurances})

def police(request):
    return render(request, 'police.html')

def repair(request):
    repairs = Repair.objects.all()
    return render(request, 'repair.html', {'repairs': repairs})
    