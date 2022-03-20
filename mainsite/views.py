from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import random
from datetime import datetime, timedelta


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
    return render(request, 'repair.html')

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
        years = int(request.POST.get('years'))
        end_date = datetime.now() + timedelta(days=365*years)

        if not user:     
            user = User.objects.create(email=email, password=password, is_customer=True, username=email)
            user.set_password(password)
            user.save()
            # sucessfully bought product
            insurance = Insurance.objects.create(user=user, product=product, description='Bought product', end_date=end_date,
                    is_claimed=False, is_approved=False, is_declined=False, claim_type=None, duration=years)
            hash_value = random.getrandbits(128)
            print("hash value: %032x" % hash_value)
            return render(request, 'register.html', {'user': user, 'insurance': insurance})        
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                if not user.is_customer:
                    return render(request, 'buy.html', {'error': 'You are not a customer!', 'product': product})
                else:
                    # sucessfully bought product
                    insurance = Insurance.objects.create(user=user, product=product, description='Bought product', end_date=end_date,
                        is_claimed=False, is_approved=False, is_declined=False, claim_type=None, duration=years)
                    hash_value = random.getrandbits(128)
                    print("hash value: %032x" % hash_value)
                    return render(request, 'reciept.html', {'user': user, 'insurance': insurance})
            else:
                return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})
    else:
        return render(request, 'buy.html', {'error': 'Wrong email or password!', 'product': product})

@csrf_exempt
def buy_register(request):
    if request.method == 'POST':
        # get first name last name and phone number
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        user = User.objects.get(id=request.POST.get('user_id'))
        insurance = Insurance.objects.get(id=request.POST.get('insurance_id'))
        # update user
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.save()
        
        return render(request, 'reciept.html', {'user': user, 'insurance': insurance})
        
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
                # all theft and repair is_approved = True 
                is_approved = list(Repair.objects.filter(is_approved=True))+list(Theft.objects.filter(is_approved=True))
                for completed in range(len(is_approved)):
                    is_approved[completed] = is_approved[completed].insurance
                # all declined claim
                is_declined = list(Repair.objects.filter(is_declined=True))+list(Theft.objects.filter(is_declined=True))
                for declined in range(len(is_declined)):
                    is_declined[declined] = is_declined[declined].insurance

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

        if claim_type == 'police':
            theft = Theft.objects.create(insurance=insurance, description=description,
                is_approved=False, is_declined=False)
        else :
            repair = Repair.objects.create(insurance=insurance, description=description,
                is_approved=False, is_declined=False)

        hash_value = random.getrandbits(128)
        print("hash value: %032x" % hash_value)
        
        return render(request, 'claim.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def insurance_disapprove(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.is_declined = True
        insurance.save()
        return render(request, 'disapproved.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def insurance_approve(request):
    if request.method == 'POST':
        insurance_id = request.POST.get('insurance_id')
        insurance = Insurance.objects.get(id=insurance_id)
        insurance.is_approved = True
        insurance.save()
        return render(request, 'approved.html', {'insurance': insurance})
    else:
        return render(request, 'insurance.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def police_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        
        if not user:     
            return render(request, 'police.html', {'error': 'Wrong email or password!'})
        
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_police:
                # all pending cases
                is_pending = Theft.objects.filter(is_approved=False, is_declined=False)
                # all solved cases
                is_solved = Theft.objects.filter(is_approved=True)|Theft.objects.filter(is_declined=True)
                return render(request, 'police_agent.html', {'is_pending': is_pending, 'is_solved': is_solved})
        
        return render(request, 'police.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def repair_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        
        if not user:     
            return render(request, 'repair.html', {'error': 'Wrong email or password!'})
        
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_repair:
                # all pending cases
                is_pending = Repair.objects.filter(is_approved=False, is_declined=False)
                # all solved cases
                is_completed = Repair.objects.filter(is_approved=True)|Repair.objects.filter(is_declined=True)
                return render(request, 'repair_agent.html', {'is_pending': is_pending, 'is_completed': is_completed})
        
        return render(request, 'repair.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def repair_approved(request):
    if request.method == 'POST':
        repair_id = request.POST.get('repair_id')
        repair = Repair.objects.get(id=repair_id)
        repair.is_approved = True
        repair.save()

        hash_value = random.getrandbits(128)
        print("hash value: %032x" % hash_value)
    
        return render(request, 'repair_approved.html', {'repair': repair})
    else:
        return render(request, 'police.html', {'error': 'Wrong email or password!'})
    
@csrf_exempt    
def repair_declined(request):
    if request.method == 'POST':
        repair_id = request.POST.get('repair_id')
        repair = Repair.objects.get(id=repair_id)
        repair.is_declined = True
        repair.save()

        hash_value = random.getrandbits(128)
        print("hash value: %032x" % hash_value)
    
        return render(request, 'repair_declined.html', {'repair': repair})
    else:
        return render(request, 'police.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def police_approved(request):
    if request.method == 'POST':
        theft_id = request.POST.get('theft_id')
        theft = Theft.objects.get(id=theft_id)
        theft.is_approved = True
        theft.save()

        hash_value = random.getrandbits(128)
        print("hash value: %032x" % hash_value)
    
        return render(request, 'police_approved.html', {'theft': theft})
    else:
        return render(request, 'police.html', {'error': 'Wrong email or password!'})

@csrf_exempt
def police_declined(request):
    if request.method == 'POST':
        theft_id = request.POST.get('theft_id')
        theft = Theft.objects.get(id=theft_id)
        theft.is_declined = True
        theft.save()

        hash_value = random.getrandbits(128)
        print("hash value: %032x" % hash_value)
    
        return render(request, 'police_declined.html', {'theft': theft})
    else:
        return render(request, 'police.html', {'error': 'Wrong email or password!'})