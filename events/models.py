from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    venue = models.CharField(max_length=300)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rsvp_deadline = models.DateTimeField()
    mpesa_paybill = models.CharField(max_length=20, blank=True)
    mpesa_account = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name

    @property
    def is_rsvp_open(self):
        from django.utils import timezone
        return timezone.now() <= self.rsvp_deadline