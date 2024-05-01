from django.shortcuts import render
from kasa.models import Sale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'login.html')

def get_sales_from_all_databases():
    all_sales = []

    sales_d1 = Sale.objects.using('d1').all()
    all_sales.extend(sales_d1)
    sales_d1 = Sale.objects.using('d2').all()
    all_sales.extend(sales_d1)
    sales_d1 = Sale.objects.using('d3').all()
    all_sales.extend(sales_d1)
    sales_d1 = Sale.objects.using('d4').all()
    all_sales.extend(sales_d1)

    return all_sales

@login_required
def manager(request):
    combined_sales = get_sales_from_all_databases()
    return render(request, 'manager.html', {'items': combined_sales,  'euro':settings.EURO, 'dollar':settings.DOLLAR})

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    def post(self, request, format=None):
        os.remove(os.path.join('', str(request.FILES.get('file'))))
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
