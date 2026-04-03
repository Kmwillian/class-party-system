from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('rsvp_entry', 'method', 'status', 'amount', 'mpesa_receipt_number', 'paid_at', 'created_at')
    list_filter = ('method', 'status')
    search_fields = ('rsvp_entry__full_name', 'rsvp_entry__registration_number', 'mpesa_receipt_number')
    readonly_fields = ('created_at', 'updated_at', 'mpesa_checkout_id', 'mpesa_receipt_number')