# chats/middleware.py

import logging
from datetime import datetime

# Set up logger
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

# File handler that writes to requests.log
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)

# Prevent duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        return self.get_response(request)

        # chats/middleware.py

from django.http import HttpResponseForbidden

class BlockUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_agents = ['curl', 'Postman', 'httpie']

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        for blocked in self.blocked_agents:
            if blocked.lower() in user_agent.lower():
                return HttpResponseForbidden("Access denied: User-Agent blocked.")
        return self.get_response(request)
# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Block access if it's NOT between 6PM (18) and 9PM (21)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chats is only allowed between 6PM and 9PM.")

        return self.get_response(request)

        # chats/middleware.py
import time
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # Format: {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        # Only limit POST requests (e.g., sending messages)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 60 seconds = 1 minute
            max_messages = 5

            if ip not in self.message_log:
                self.message_log[ip] = []

            # Remove old timestamps (outside time window)
            self.message_log[ip] = [
                t for t in self.message_log[ip] if now - t < window
            ]

            if len(self.message_log[ip]) >= max_messages:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            # Log this new message
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract IP from headers or META"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated, skip
        if not request.user.is_authenticated:
            return HttpResponseForbidden("403 Forbidden: Authentication required.")

        # Check user role (using Django groups or staff status)
        if not (request.user.is_superuser or request.user.groups.filter(name__in=["admin", "moderator"]).exists()):
            return HttpResponseForbidden("403 Forbidden: You do not have permission to perform this action.")

        return self.get_response(request)
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated, skip
        if not request.user.is_authenticated:
            return HttpResponseForbidden("403 Forbidden: Authentication required.")

        # Check user role (using Django groups or staff status)
        if not (request.user.is_superuser or request.user.groups.filter(name__in=["admin", "moderator"]).exists()):
            return HttpResponseForbidden("403 Forbidden: You do not have permission to perform this action.")

        return self.get_response(request)


