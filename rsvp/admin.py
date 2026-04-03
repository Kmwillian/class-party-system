from django.contrib import admin
from .models import RSVPEntry


@admin.register(RSVPEntry)
class RSVPEntryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'registration_number', 'phone_number', 'event', 'is_attending', 'has_paid', 'created_at')
    list_filter = ('is_attending', 'event')
    search_fields = ('full_name', 'registration_number', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')