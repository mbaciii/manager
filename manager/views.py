import time

from django.shortcuts import render
from kasa.models import Sale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os, requests


def menu(request):
    # Paths to the menu images
    albanian_menu_image = "/static/englishf.png"
    english_menu_image = "/static/albanianf.png"

    return render(request, 'menu2.html', {
        'albanian_menu_image': albanian_menu_image,
        'english_menu_image': english_menu_image
    })



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
    sales_d1 = Sale.objects.using('d5').all()
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
import os
import requests
import tempfile
import shutil
import time
from django.core.exceptions import SuspiciousFileOperation

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    def post(self, request, format=None):

        USERNAME = 'mbaci'
        API_TOKEN = '3ab87b4e1b23b1bef66739b12f32cfd913a70827'
        API_URL = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/files/path/'
        file_name = request.FILES.get('file').name
        file_path = '/home/mbaci/manager/' + file_name
        file_name_prefix = file_name.split('.')[0]  # Extracting filename prefix without extension

        # Lock file to prevent simultaneous access
        lock_file_path = file_path + '.lock'
        while os.path.exists(lock_file_path):
            time.sleep(0.1)  # Wait for lock file to be released
        open(lock_file_path, 'w').close()  # Create lock file

        try:
            # Send a DELETE request to delete the file
            response = requests.delete(API_URL + file_path, headers={'Authorization': f'Token {API_TOKEN}'})

            # Check if the request was successful
            if response.status_code == 204:
                print("File deleted successfully.")
            else:
                print("Failed to delete file. Status code:", response.status_code)

            # Write the content of the POST request to a temporary file
            temp_file_path = tempfile.mktemp(dir='/home/mbaci/manager/')
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(request.FILES['file'].read())

            # Move the temporary file to the final location atomically
            shutil.move(temp_file_path, file_path)
            print("File replaced successfully.")

            # Clean up lock file
            os.remove(lock_file_path)

            file_serializer = UploadedFileSerializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save()
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Failed to replace file:", str(e))
            # Clean up lock file
            os.remove(lock_file_path)
            return Response({'error': 'Failed to replace file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Cleanup additional files with similar filename prefixes
            for filename in os.listdir('/home/mbaci/manager/'):
                if filename.startswith(file_name_prefix) and filename != file_name:
                    os.remove(os.path.join('/home/mbaci/manager/', filename))