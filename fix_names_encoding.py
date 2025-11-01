"""
Виправлення кодування імен та прізвищ користувачів
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User


def fix_double_encoded_string(text):
    """
    Виправляє подвійне кодування UTF-8 -> latin1 -> UTF-8
    """
    if not text:
        return text

    try:
        # Спроба декодувати UTF-8 як latin-1 і закодувати назад як UTF-8
        fixed = text.encode('latin-1').decode('utf-8')
        return fixed
    except (UnicodeDecodeError, UnicodeEncodeError):
        # Якщо не вдалося - текст вже правильний
        return text


def needs_fixing(text):
    """Перевіряє, чи потрібно виправляти текст"""
    if not text:
        return False

    # Перевірка на кракозябри (кирилиця у форматі РђРґРјС–РЅ)
    try:
        # Якщо текст містить символи з діапазону кирилиці у UTF-8, але відображається як latin-1
        encoded = text.encode('latin-1')
        decoded = encoded.decode('utf-8')
        # Якщо декодування успішне і результат відрізняється - потрібно виправлення
        return decoded != text
    except (UnicodeDecodeError, UnicodeEncodeError):
        return False


def fix_all_users():
    """Виправлення всіх користувачів"""
    users = User.objects.all()
    fixed_count = 0

    print("Початок виправлення імен користувачів...\n")

    for user in users:
        changed = False

        # Виправлення імені
        if user.first_name and needs_fixing(user.first_name):
            old_name = user.first_name
            user.first_name = fix_double_encoded_string(user.first_name)
            print(f"✓ {user.username}: Ім'я '{old_name}' -> '{user.first_name}'")
            changed = True

        # Виправлення прізвища
        if user.last_name and needs_fixing(user.last_name):
            old_surname = user.last_name
            user.last_name = fix_double_encoded_string(user.last_name)
            print(f"✓ {user.username}: Прізвище '{old_surname}' -> '{user.last_name}'")
            changed = True

        if changed:
            user.save()
            fixed_count += 1

    print(f"\n{'='*70}")
    print(f"Виправлено {fixed_count} користувачів")
    print(f"{'='*70}")

    # Перевірка результатів
    print("\nПеревірка результатів:\n")
    for user in User.objects.all()[:5]:  # Перші 5 для прикладу
        print(f"{user.username}: {user.get_full_name()} ({user.profile.get_role_display()})")


if __name__ == '__main__':
    fix_all_users()
    print("\n✓ Готово! Оновіть сторінку в браузері.")
