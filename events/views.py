from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm


@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_create(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('events:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.name}" updated successfully!')
            return redirect('events:list')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event', 'event': event})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})