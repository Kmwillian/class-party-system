from django.db import models
from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    is_class_rep = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username}"