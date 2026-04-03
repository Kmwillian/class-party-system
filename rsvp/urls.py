from django.urls import path
from . import views

app_name = 'rsvp'

urlpatterns = [
    path('', views.rsvp_home, name='home'),
    path('register/', views.rsvp_register, name='register'),
    path('success/<int:pk>/', views.rsvp_success, name='success'),
    path('list/', views.rsvp_list, name='list'),
    path('export/', views.export_rsvp_csv, name='export'),
]