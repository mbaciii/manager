
from django.urls import path
from . import views

urlpatterns = [
    path('kasa/', views.cashier_view, name='cashier_view'),
    path('register-sale/', views.register_sale, name='register_sale'),  # Add this line
    path('perditesim/', views.perditesim, name='perditesim'),

]
