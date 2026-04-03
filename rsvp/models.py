from django.db import models
from events.models import Event


class RSVPEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvp_entries')
    full_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    is_attending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'RSVP Entry'
        verbose_name_plural = 'RSVP Entries'
        unique_together = ('event', 'registration_number')

    def __str__(self):
        return f"{self.full_name} — {self.registration_number}"

    @property
    def has_paid(self):
        return self.payments.filter(status='completed').exists()

    @property
    def payment_status(self):
        payment = self.payments.filter(status='completed').first()
        if payment:
            return payment.method
        return 'unpaid'