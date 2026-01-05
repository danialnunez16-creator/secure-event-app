from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='/accounts/profile/'), name='password_change'),
    
    # Events
    path('', views.event_list, name='event_list'),
    path('request/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/register/', views.event_register, name='event_register'),
    path('event/<int:event_id>/confirmation/', views.event_confirmation, name='event_confirmation'),
    
    # Security / Admin
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('event/<int:event_id>/edit/', views.event_update, name='event_update'),
    path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('registration/<int:registration_id>/delete/', views.registration_delete, name='registration_delete'),
    path('security/audit-logs/', views.audit_log_list, name='audit_log_list'),
]
