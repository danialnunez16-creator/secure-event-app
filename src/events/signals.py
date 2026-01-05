from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from .models import AuditLog
import logging

logger = logging.getLogger('events.security')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    AuditLog.objects.create(
        user=user,
        action='LOGIN',
        ip_address=ip,
        details=f"User {user.username} logged in successfully."
    )
    logger.info(f"Login success: {user.username} from {ip}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    username = credentials.get('username', 'unknown')
    AuditLog.objects.create(
        action='LOGIN_FAILED',
        ip_address=ip,
        details=f"Failed login attempt for username: {username}"
    )
    logger.warning(f"Login failed: {username} from {ip}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user:
        ip = get_client_ip(request)
        AuditLog.objects.create(
            user=user,
            action='LOGOUT',
            ip_address=ip,
            details=f"User {user.username} logged out."
        )
        logger.info(f"Logout: {user.username} from {ip}")
