"""
Тест швидкості входу (виведення у файл)
"""
import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings

output_file = 'login_speed_test.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("Тест швидкості входу\n")
    f.write("=" * 70 + "\n\n")

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
            f.write(f"[OK] {username}: {elapsed:.0f} ms - успішна аутентифікація\n")
        else:
            f.write(f"[FAIL] {username}: {elapsed:.0f} ms - помилка аутентифікації\n")

    f.write("\n" + "=" * 70 + "\n")
    f.write("Налаштування хешування паролів:\n")

    if hasattr(settings, 'PASSWORD_HASHERS'):
        for i, hasher in enumerate(settings.PASSWORD_HASHERS, 1):
            f.write(f"  {i}. {hasher}\n")
    else:
        f.write("  Використовуються стандартні налаштування Django\n")

    # Перевірка типу хешу
    admin = User.objects.filter(username='admin').first()
    if admin:
        f.write(f"\nПриклад збереженого пароля: {admin.password[:60]}...\n")
        hasher_type = admin.password.split('$')[0] if '$' in admin.password else 'unknown'
        f.write(f"Тип хешера: {hasher_type}\n")

print(f"Результати збережено у файл: {output_file}")
