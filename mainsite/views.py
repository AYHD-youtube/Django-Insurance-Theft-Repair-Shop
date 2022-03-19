from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import random


# Create your views here.
def index(request):
    return render(request, 'index.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def insurance(request):
    return render(request, 'insurance.html')

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
            user.set_password(password)
            user.save()
            # sucessfully bought product
            Insurance.objects.create(user=user, product=product, description='Bought product', is_claimed=False, is_approved=False, is_declined=False)
            hash_value = random.getrandbits(128)
            print("hash value: %032x" % hash_value)
            return render(request, 'reciept.html', {'user': user, 'product': product})        
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                if not user.is_customer:
                    return render(request, 'buy.html', {'error': 'You are not a customer!', 'product': product})
                else:
                    # sucessfully bought product
                    Insurance.objects.create(user=user, product=product, description='Bought product', is_claimed=False, is_approved=False, is_declined=False)
                    hash_value = random.getrandbits(128)
                    print("hash value: %032x" % hash_value)
                    return render(request, 'reciept.html', {'user': user, 'product': product})
            else:
                return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})
    else:
        return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})

@csrf_exempt      
def insurance_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        
        if not user:     
            return render(request, 'insurance.html', {'error': 'Wrong email or password!'})
        
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_insurance:
                # all pending claim
                is_pending = Insurance.objects.filter( is_claimed=True, is_approved=False, is_declined=False)
                # all approved claim
                is_approved = Insurance.objects.filter(is_claimed=True, is_approved=True, is_declined=False)
                # all declined claim
                is_declined = Insurance.objects.filter(is_claimed=True, is_approved=False, is_declined=True)
                return render(request, 'insurance_agent.html', {'is_pending': is_pending, 'is_approved': is_approved, 'is_declined': is_declined})

            else:
                # all pending claims
                is_pending = Insurance.objects.filter(user=user, is_claimed=True, is_approved=False, is_declined=False)
                # all is_approved = True
                is_approved = Insurance.objects.filter(user=user, is_approved=True)
                # all isurance bought not claimed and approved
                is_bought = Insurance.objects.filter(user=user, is_claimed=False, is_approved=False, is_declined=False)
                # all declined claims
                is_declined = Insurance.objects.filter(user=user, is_declined=True)

                return render(request, 'insurance_customer.html', {'user': user, 'is_pending': is_pending, 'is_approved': is_approved, 'is_bought': is_bought
                , 'is_declined': is_declined})

    return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def claim_insurance(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        insurance = Insurance.objects.get(id=insurance_id)
        return render(request, 'claim_insurance.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})
    
@csrf_exempt
def claim_submit(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        description = request.POST.get('reason')
        claim_type = request.POST.get('type')
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.is_claimed = True
        insurance.description = description
        insurance.claim_type = claim_type
        insurance.save()
        return render(request, 'claim.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def insurance_disapprove(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        insurance = Insurance.objects.get(id=insurance_id)
        return render(request, 'insurance_disapprove.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def insurance_approve(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        insurance = Insurance.objects.get(id=insurance_id)
        return render(request, 'insurance_approve.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def approve(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        description = request.POST.get('reason')
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.is_approved = True
        insurance.description = insurance.description + description
        insurance.save()
        return render(request, 'approved.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def disapprove(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        description = request.POST.get('reason')
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.is_declined = True
        insurance.description = insurance.description + description
        insurance.save()
        return render(request, 'disapproved.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})