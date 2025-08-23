# messaging_app/urls.py

"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.shortcuts import redirect

def home_view(request):
    return HttpResponse("""
    <h1>🎉 Messaging App is Running Successfully!</h1>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><a href="/api/v1/">/api/v1/</a> - API Root</li>
        <li><a href="/api/v1/conversations/">/api/v1/conversations/</a> - Conversations</li>
        <li><a href="/admin/">/admin/</a> - Django Admin</li>
        <li><a href="/api-auth/">/api-auth/</a> - API Authentication</li>
    </ul>
    <p><strong>Your Django messaging app Docker container is working perfectly!</strong></p>
    """)

urlpatterns = [
    path("", home_view, name="home"),  # Home page
    path("admin/", admin.site.urls),
    path("api/v1/", include("chats.urls")),
    path('api-auth/', include('rest_framework.urls')),  # DRF auth for browseable API
]
