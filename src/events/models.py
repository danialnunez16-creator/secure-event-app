from django.conf import settings
from django.db import models
from django.utils import timezone

class AuditLog(models.Model):
    ACTION_TYPES = (
        ('LOGIN', 'Login'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('LOGOUT', 'Logout'),
        ('REGISTER', 'User Registration'),
        ('CREATE_EVENT', 'Create Event'),
        ('UPDATE_EVENT', 'Update Event'),
        ('DELETE_EVENT', 'Delete Event'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_at = models.DateTimeField()   # tarikh & masa event
    capacity = models.PositiveIntegerField(default=50)
    location = models.CharField(max_length=200, blank=True, null=True)  # lokasi event
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="events_created"
    )

    def __str__(self):
        return self.title

    @property
    def seats_left(self):
        # kira baki tempat berdasarkan jumlah registration
        return max(0, self.capacity - self.registrations.count())


class Registration(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations"
    )
    registered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("email", "event")  # elak peserta sama daftar event sama dua kali

    def __str__(self):
        return f"{self.name} -> {self.event}"
