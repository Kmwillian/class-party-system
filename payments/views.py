import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Payment
from .forms import MarkCashPaidForm
from .mpesa import stk_push
from rsvp.models import RSVPEntry
from events.models import Event


def initiate_mpesa_payment(request, rsvp_pk):
    rsvp = get_object_or_404(RSVPEntry, pk=rsvp_pk)
    event = rsvp.event

    if rsvp.has_paid:
        messages.info(request, 'This RSVP has already been paid.')
        return redirect('rsvp:success', pk=rsvp.pk)

    payment = Payment.objects.create(
        rsvp_entry=rsvp,
        method='mpesa',
        status='pending',
        amount=event.contribution_amount,
        phone_number=rsvp.phone_number,
    )

    response = stk_push(
        phone_number=rsvp.phone_number,
        amount=event.contribution_amount,
        account_reference=rsvp.registration_number,
        description=f'Party contribution for {event.name}',
    )

    if response.get('ResponseCode') == '0':
        payment.mpesa_checkout_id = response.get('CheckoutRequestID', '')
        payment.save()
        messages.success(request, 'M-Pesa payment request sent! Check your phone and enter your PIN.')
    else:
        payment.status = 'failed'
        payment.save()
        messages.error(request, 'M-Pesa request failed. Please try again or pay cash.')

    return redirect('payments:status', pk=payment.pk)


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        callback = data.get('Body', {}).get('stkCallback', {})
        checkout_id = callback.get('CheckoutRequestID')
        result_code = callback.get('ResultCode')

        try:
            payment = Payment.objects.get(mpesa_checkout_id=checkout_id)
            if result_code == 0:
                metadata = callback.get('CallbackMetadata', {}).get('Item', [])
                meta_dict = {item['Name']: item.get('Value') for item in metadata}
                payment.status = 'completed'
                payment.mpesa_receipt_number = meta_dict.get('MpesaReceiptNumber', '')
                payment.paid_at = timezone.now()
            else:
                payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})


def payment_status(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payments/status.html', {'payment': payment})


@login_required
def mark_cash_paid(request, rsvp_pk):
    rsvp = get_object_or_404(RSVPEntry, pk=rsvp_pk)

    if rsvp.has_paid:
        messages.info(request, f'{rsvp.full_name} has already been marked as paid.')
        return redirect('rsvp:list')

    form = MarkCashPaidForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            payment = form.save(commit=False)
            payment.rsvp_entry = rsvp
            payment.method = 'cash'
            payment.status = 'completed'
            payment.amount = rsvp.event.contribution_amount
            payment.paid_at = timezone.now()
            payment.save()
            messages.success(request, f'{rsvp.full_name} marked as paid successfully!')
            return redirect('rsvp:list')

    return render(request, 'payments/mark_cash.html', {'form': form, 'rsvp': rsvp})


@login_required
def payment_list(request):
    payments = Payment.objects.filter(status='completed').select_related('rsvp_entry')
    total = payments.count()
    total_amount = sum(p.amount for p in payments)

    return render(request, 'payments/payment_list.html', {
        'payments': payments,
        'total': total,
        'total_amount': total_amount,
    })