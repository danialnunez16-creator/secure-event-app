from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_at", "capacity", "seats_left", "location", "created_by")

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "event", "registered_at")
    search_fields = ("name", "email")  # senang cari peserta
    list_filter = ("event",)           # boleh filter ikut event
