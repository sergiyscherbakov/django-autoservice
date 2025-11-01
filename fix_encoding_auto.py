"""
Скрипт для виправлення кодування в базі даних (автоматичний режим)
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
    fixed_count = 0

    for user in users:
        changed = False

        # Виправлення імені
        if user.first_name:
            try:
                # Спроба декодувати як latin-1 і закодувати як utf-8
                fixed_first_name = user.first_name.encode('latin-1').decode('utf-8')
                if fixed_first_name != user.first_name:
                    user.first_name = fixed_first_name
                    changed = True
                    print(f"Виправлено ім'я для {user.username}: {fixed_first_name}")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"Ім'я користувача {user.username} вже має правильне кодування")

        # Виправлення прізвища
        if user.last_name:
            try:
                fixed_last_name = user.last_name.encode('latin-1').decode('utf-8')
                if fixed_last_name != user.last_name:
                    user.last_name = fixed_last_name
                    changed = True
                    print(f"Виправлено прізвище для {user.username}: {fixed_last_name}")
            except (UnicodeEncodeError, UnicodeDecodeError) as e:
                print(f"Прізвище користувача {user.username} вже має правильне кодування")

        if changed:
            user.save()
            fixed_count += 1

    print(f"\nОновлено {fixed_count} користувачів.")
    return fixed_count


def verify_results():
    """Перевірка результатів"""
    print("\n" + "=" * 70)
    print("Результати після виправлення:")
    print("=" * 70)

    users = User.objects.all()
    for user in users:
        profile = user.profile
        full_name = user.get_full_name()
        role_display = profile.get_role_display()

        print(f"Користувач: {user.username}")
        print(f"  Повне ім'я: {full_name}")
        print(f"  Роль: {role_display}")
        print()


if __name__ == '__main__':
    print("=" * 70)
    print("Початок виправлення кодування...")
    print("=" * 70)

    fixed = fix_user_data()

    if fixed > 0:
        verify_results()
        print("\nГотово! Перезавантажте сторінку в браузері.")
    else:
        print("\nВиправлення не потрібні - всі дані вже мають правильне кодування.")
