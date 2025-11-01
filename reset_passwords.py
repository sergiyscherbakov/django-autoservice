"""
Скидання паролів користувачів (оновлення хешів з новими налаштуваннями)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User

# Список користувачів та їх паролі (зі створення тестових даних)
users_passwords = {
    'admin': '123',
    'mechanic1': '123',
    'mechanic2': '123',
    'client1': '123',
    'client2': '123',
    'client3': '123',
    'sergiy': '123',
    'ivan_petrenko': 'password123',
    'maria_kovalenko': 'password123',
    'oleh_shevchenko': 'password123',
    'anna_bondar': 'password123',
    'petro_melnyk': 'password123',
    'vasyl_mechanic': 'password123',
    'dmytro_master': 'password123',
    'andriy_technician': 'password123',
    'admin_user': 'admin123',
}

print("Оновлення паролів користувачів...")
print("=" * 70)

updated = 0
not_found = 0

for username, password in users_passwords.items():
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"[OK] {username} - пароль оновлено")
        updated += 1
    except User.DoesNotExist:
        print(f"[SKIP] {username} - користувача не знайдено")
        not_found += 1

print("=" * 70)
print(f"Оновлено: {updated}")
print(f"Не знайдено: {not_found}")
print("\nТепер спробуйте увійти з цими обліковими даними:")
print("  admin / 123")
print("  client1 / 123")
print("  mechanic1 / 123")
