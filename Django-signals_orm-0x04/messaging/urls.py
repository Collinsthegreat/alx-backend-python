from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_chat.urls')),  # ✅ include the app's URLs
]
"""
urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),  # ✅ Add this
]
"""

urlpatterns = [
    path('conversation/<int:user_id>/', views.conversation_view, name='conversation_view'),
    path('delete_user/', views.delete_user, name='delete_user'),
]