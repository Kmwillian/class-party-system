from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'contribution_amount', 'is_active', 'is_rsvp_open')
    list_filter = ('is_active',)
    search_fields = ('name', 'venue')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)