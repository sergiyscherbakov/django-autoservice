"""
Скрипт для виправлення кодування в базі даних
"""
import os
import django

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User
from service.models import UserProfile


def fix_user_data():
    """Виправлення кодування для користувачів"""
    users = User.objects.all()

    for user in users:
        # Виправлення імені
        if user.first_name:
            try:
                # Спроба декодувати як latin-1 і закодувати як utf-8
                fixed_first_name = user.first_name.encode('latin-1').decode('utf-8')
                user.first_name = fixed_first_name
                print(f"Виправлено ім'я: {user.username} -> {fixed_first_name}")
            except (UnicodeEncodeError, UnicodeDecodeError):
                print(f"Ім'я користувача {user.username} вже правильне")

        # Виправлення прізвища
        if user.last_name:
            try:
                fixed_last_name = user.last_name.encode('latin-1').decode('utf-8')
                user.last_name = fixed_last_name
                print(f"Виправлено прізвище: {user.username} -> {fixed_last_name}")
            except (UnicodeEncodeError, UnicodeDecodeError):
                print(f"Прізвище користувача {user.username} вже правильне")

        user.save()

    print("\nГотово! Всі дані користувачів оновлено.")


def check_current_encoding():
    """Перевірка поточного кодування"""
    print("Перевірка поточних даних:\n")
    users = User.objects.all()

    for user in users:
        profile = user.profile
        print(f"Користувач: {user.username}")
        print(f"  Ім'я: {user.first_name}")
        print(f"  Прізвище: {user.last_name}")
        print(f"  Роль (код): {profile.role}")
        print(f"  Роль (відображення): {profile.get_role_display()}")
        print(f"  Повне ім'я: {user.get_full_name()}")
        print()


if __name__ == '__main__':
    print("=" * 50)
    print("Перевірка даних до виправлення:")
    print("=" * 50)
    check_current_encoding()

    response = input("\nПродовжити виправлення? (yes/no): ")
    if response.lower() in ['yes', 'y', 'так']:
        print("\n" + "=" * 50)
        print("Виправлення даних:")
        print("=" * 50)
        fix_user_data()

        print("\n" + "=" * 50)
        print("Перевірка даних після виправлення:")
        print("=" * 50)
        check_current_encoding()
    else:
        print("Скасовано.")
