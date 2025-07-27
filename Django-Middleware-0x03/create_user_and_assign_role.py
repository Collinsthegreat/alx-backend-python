"""from django.contrib.auth.models import User, Group
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Middleware_0x03.settings')
django.setup()

# Create a user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()
    print("✅ User created.")
else:
    print("ℹ️ User already exists.")

# Create admin group
admin_group, _ = Group.objects.get_or_create(name='admin')

# Add user to group
user.groups.add(admin_group)
print(f"✅ User '{user.username}' added to group '{admin_group.name}'.")
"""
"""
import os
import django

# 🔧 Set environment to point to your settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Middleware_0x03.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')


# ✅ Setup Django
django.setup()

# ⬇️ Now import Django models
from django.contrib.auth.models import User, Group

# ✅ Create groups
admin_group, _ = Group.objects.get_or_create(name='admin')
moderator_group, _ = Group.objects.get_or_create(name='moderator')

# ✅ Create a test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()
    print("✅ User created.")
else:
    print("ℹ️ User already exists.")

# ✅ Add user to 'admin' group
user.groups.add(admin_group)
print(f"✅ User '{user.username}' added to group '{admin_group.name}'.")
"""

import os
import django

# Set environment to point to your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

# Setup Django
django.setup()

# Import Django models
from django.contrib.auth.models import User, Group

# Create groups
admin_group, _ = Group.objects.get_or_create(name='admin')
moderator_group, _ = Group.objects.get_or_create(name='moderator')

# Create a test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()
    print("User created.")
else:
    print("User already exists.")

# Add user to 'admin' group
user.groups.add(admin_group)
print(f"User '{user.username}' added to group '{admin_group.name}'.")
