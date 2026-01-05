from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .models import Event, Registration, AuditLog
from .forms import CustomUserCreationForm, UserProfileForm, EventForm, RegistrationForm

def is_admin(user):
    return user.is_authenticated and user.is_superuser

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@ratelimit(key='ip', rate='3/m', block=True)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('event_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register_user.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'events/profile.html', {'form': form})

@login_required
def audit_log_list(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')
    return render(request, 'events/audit_log_list.html', {'logs': logs})

def event_list(request):
    events = Event.objects.all().order_by('start_at')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_create(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created.")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': f'Edit {event.title}'})

@login_required
def event_register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if event.seats_left > 0:
                registration = form.save(commit=False)
                registration.event = event
                registration.save()
                messages.success(request, "Successfully registered!")
                return redirect('event_confirmation', event_id=event.id)
            else:
                messages.error(request, "Event is full.")
    else:
        initial = {'email': request.user.email, 'name': request.user.get_full_name()} if request.user.is_authenticated else {}
        form = RegistrationForm(initial=initial)
    return render(request, 'events/event_register.html', {'event': event, 'form': form})

@login_required
def event_confirmation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    # Get the latest registration for this user (by email) and event
    registration = Registration.objects.filter(email=request.user.email, event=event).last() if request.user.is_authenticated else None
    
    return render(request, 'events/event_confirmation.html', {'event': event, 'registration': registration})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    # Prefetch registrations to avoid N+1 queries
    events = Event.objects.prefetch_related('registrations').order_by('-start_at')
    
    total_events = events.count()
    total_registrations = Registration.objects.count()
    
    context = {
        'events': events,
        'total_events': total_events,
        'total_registrations': total_registrations
    }
    return render(request, 'events/admin_dashboard.html', context)

@login_required
def event_delete(request, event_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, f"Event '{event.title}' has been deleted.")
    return redirect('admin_dashboard')

@login_required
def registration_delete(request, registration_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    registration = get_object_or_404(Registration, pk=registration_id)
    if request.method == 'POST':
        event_title = registration.event.title
        registration.delete()
        messages.success(request, f"Registration for {registration.name} deleted from {event_title}.")
    return redirect('admin_dashboard')
