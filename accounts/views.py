from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count

from .forms import AdminLoginForm
from rsvp.models import RSVPEntry
from payments.models import Payment
from events.models import Event


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = AdminLoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Welcome back, {form.get_user().get_full_name() or form.get_user().username}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    event = Event.objects.filter(is_active=True).first()

    total_rsvp = RSVPEntry.objects.filter(is_attending=True).count()
    total_paid = Payment.objects.filter(status='completed').count()
    total_pending = total_rsvp - total_paid
    total_collected = Payment.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    recent_rsvps = RSVPEntry.objects.filter(
        is_attending=True
    ).order_by('-created_at')[:10]

    recent_payments = Payment.objects.filter(
        status='completed'
    ).order_by('-paid_at')[:10]

    context = {
        'event': event,
        'total_rsvp': total_rsvp,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_collected': total_collected,
        'recent_rsvps': recent_rsvps,
        'recent_payments': recent_payments,
    }
    return render(request, 'accounts/dashboard.html', context)