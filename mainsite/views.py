import email
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

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

@csrf_exempt
def buy(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        return render(request, 'buy.html', {'product': product})
    else:
        return render(request, 'shop.html')

@csrf_exempt
def buy_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        product = Product.objects.get(id=request.POST.get('product_id'))
        if not user:     
            user = User.objects.create(email=email, password=password, is_customer=True, username=email)
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                if not user.is_customer:
                    return render(request, 'buy.html', {'error': 'You are not a customer!', 'product': product})
                else:
                    return render(request, 'reciept.html', {'user': user, 'product': product})
            else:
                return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})
    else:
        return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})
        