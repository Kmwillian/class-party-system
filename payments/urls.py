from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:rsvp_pk>/', views.initiate_mpesa_payment, name='mpesa_pay'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    path('status/<int:pk>/', views.payment_status, name='status'),
    path('cash/<int:rsvp_pk>/', views.mark_cash_paid, name='mark_cash'),
    path('list/', views.payment_list, name='list'),
]