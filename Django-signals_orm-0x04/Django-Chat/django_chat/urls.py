from django.urls import path
from . import views

urlpatterns = [
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
]

urlpatterns = [
    path('delete-account/', views.delete_user, name='delete_user'),
]
