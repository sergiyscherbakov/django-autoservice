"""
Тест швидкості входу та хешування паролів
"""
import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Тест аутентифікації
print("Тест швидкості входу...")
print("=" * 70)

test_users = [
    ('admin', '123'),
    ('client1', '123'),
    ('mechanic1', '123'),
]

for username, password in test_users:
    start_time = time.time()
    user = authenticate(username=username, password=password)
    end_time = time.time()

    elapsed = (end_time - start_time) * 1000  # в мілісекундах

    if user:
        print(f"✓ {username}: {elapsed:.2f} ms - УСПІШНО")
    else:
        print(f"✗ {username}: {elapsed:.2f} ms - ПОМИЛКА")

print("\n" + "=" * 70)

# Перевірка налаштувань хешування
from django.conf import settings

print("\nНалаштування хешування паролів:")
if hasattr(settings, 'PASSWORD_HASHERS'):
    for i, hasher in enumerate(settings.PASSWORD_HASHERS, 1):
        print(f"  {i}. {hasher}")
else:
    print("  Використовуються стандартні налаштування Django")

# Перевірка першого користувача
admin = User.objects.filter(username='admin').first()
if admin:
    print(f"\nПароль admin збережено як: {admin.password[:50]}...")
    hasher_type = admin.password.split('$')[0] if '$' in admin.password else 'unknown'
    print(f"Тип хешера: {hasher_type}")
