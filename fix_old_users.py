"""
Виправлення кодування для старих користувачів
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User

# Список користувачів зі старими даними та правильні значення
CORRECT_NAMES = {
    'admin': {'first_name': 'Адмін', 'last_name': 'Адміністратор'},
    'mechanic1': {'first_name': 'Іван', 'last_name': 'Петренко'},
    'mechanic2': {'first_name': 'Олег', 'last_name': 'Сидоренко'},
    'client1': {'first_name': 'Марія', 'last_name': 'Коваленко'},
    'client2': {'first_name': 'Андрій', 'last_name': 'Шевченко'},
    'client3': {'first_name': 'Олена', 'last_name': 'Бондаренко'},
}

def fix_specific_users():
    """Виправлення конкретних користувачів"""
    fixed_count = 0

    for username, names in CORRECT_NAMES.items():
        try:
            user = User.objects.get(username=username)

            old_first = user.first_name
            old_last = user.last_name

            user.first_name = names['first_name']
            user.last_name = names['last_name']
            user.save()

            print(f"[OK] {username}:")
            print(f"     {old_first} -> {user.first_name}")
            print(f"     {old_last} -> {user.last_name}")
            print()

            fixed_count += 1
        except User.DoesNotExist:
            print(f"[SKIP] Користувача {username} не знайдено")

    return fixed_count


if __name__ == '__main__':
    print("=" * 70)
    print("Виправлення кодування імен користувачів")
    print("=" * 70)
    print()

    fixed = fix_specific_users()

    print("=" * 70)
    print(f"Виправлено {fixed} користувачів")
    print("=" * 70)
    print()

    # Перевірка
    print("Перевірка результатів:")
    print("-" * 70)
    for username in CORRECT_NAMES.keys():
        try:
            user = User.objects.get(username=username)
            print(f"{username}: {user.get_full_name()} ({user.profile.get_role_display()})")
        except User.DoesNotExist:
            pass

    print()
    print("Готово! Оновіть сторінку в браузері.")
