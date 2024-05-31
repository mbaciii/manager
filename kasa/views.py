# views.py
from django.shortcuts import render
from .models import Product, Sale
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login

def euToLeke(price):
    lekep = float(price * settings.EURO)
    return lekep

def euToUSD(price):
    price = euToLeke(price)
    usdp = price * settings.DOLLAR / 10000
    return usdp

@login_required
def cashier_view(request):
    products = Product.objects.all()
    return render(request, 'kasa.html', {'products': products, 'euro':settings.EURO, 'dollar':settings.DOLLAR})

from django.shortcuts import redirect
import datetime
import json
from django.http import JsonResponse
import threading
import requests

def perditesim1(request):
    try:
        with open(r'db5.sqlite3', 'rb') as file:
            files = {'file': file}
            response = requests.post('https://mbaci.pythonanywhere.com/upload/', files=files, timeout=10)#TESTTT

        # Check the response status code
        if response.status_code == 201:
            print("POST request was successful.")
            print("Response:", response.json())
        else:
            print("POST request failed with status code:", response.status_code)
    except:
        pass
    return redirect(request.META.get('HTTP_REFERER'))

def perditesim(request):
    thread = threading.Thread(target=perditesim1, args=(request,))
    thread.start()
    return redirect(request.META.get('HTTP_REFERER'))


def register_sale(request):
    if request.method == 'POST':
        sale_items_json = request.POST.get('sale_items')
        sale_items_data = json.loads(sale_items_json)
        receipt_code = generate_receipt_code()
        for item in sale_items_data:
            product_id = item['prodID']
            price = item['price']
            # Create Sale object for each sale item
            sale = Sale.objects.create(product_id=product_id, price=price, receipt_code=receipt_code)
        # upload_script_path = os.path.join(os.path.dirname(__file__), r'C:\Users\User\store_manager\manager\uploadDB.py')
        # exec(open(upload_script_path).read())
        # print(upload_script_path)

        perditesim(request)


        return JsonResponse({'success': True, 'last_sale':sale_items_data})
    else:
        return JsonResponse({'success': False})


import uuid

def generate_receipt_code():
    prefix = 'SA'  # Prefix for the receipt code
    unique_id = uuid.uuid4().hex[:6]  # Generate a random 6-character unique ID
    return f'{prefix}-{unique_id}'

