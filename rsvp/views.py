from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
import csv

from .models import RSVPEntry
from .forms import RSVPForm
from events.models import Event


def rsvp_home(request):
    event = Event.objects.filter(is_active=True).first()
    if not event:
        return render(request, 'rsvp/no_event.html')

    return render(request, 'rsvp/home.html', {'event': event})


def rsvp_register(request):
    event = get_object_or_404(Event, is_active=True)

    if not event.is_rsvp_open:
        messages.error(request, 'Sorry, RSVP registration is now closed.')
        return redirect('rsvp:home')

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.save()
            messages.success(request, f'Thank you {rsvp.full_name}! Your RSVP has been confirmed.')
            return redirect('rsvp:success', pk=rsvp.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RSVPForm()

    return render(request, 'rsvp/register.html', {'form': form, 'event': event})


def rsvp_success(request, pk):
    rsvp = get_object_or_404(RSVPEntry, pk=pk)
    return render(request, 'rsvp/success.html', {'rsvp': rsvp, 'event': rsvp.event})


@login_required
def rsvp_list(request):
    event = Event.objects.filter(is_active=True).first()
    entries = RSVPEntry.objects.filter(is_attending=True).select_related('event')

    status_filter = request.GET.get('status', '')
    if status_filter == 'paid':
        entries = [e for e in entries if e.has_paid]
    elif status_filter == 'unpaid':
        entries = [e for e in entries if not e.has_paid]

    context = {
        'entries': entries,
        'event': event,
        'status_filter': status_filter,
        'total': len(entries) if isinstance(entries, list) else entries.count(),
    }
    return render(request, 'rsvp/rsvp_list.html', context)


@login_required
def export_rsvp_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rsvp_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Registration Number', 'Phone Number', 'Payment Status', 'Method', 'RSVP Date'])

    entries = RSVPEntry.objects.filter(is_attending=True).order_by('full_name')
    for entry in entries:
        writer.writerow([
            entry.full_name,
            entry.registration_number,
            entry.phone_number,
            'Paid' if entry.has_paid else 'Unpaid',
            entry.payment_status,
            entry.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response