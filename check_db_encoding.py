"""
Перевірка кодування в базі даних (вивід у файл)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User
from service.models import UserProfile

# Записуємо результати у файл UTF-8
output_file = 'encoding_check.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("Перевірка кодування даних у базі\n")
    f.write("=" * 70 + "\n\n")

    # Перевірка ROLE_CHOICES
    f.write("ROLE_CHOICES з моделі UserProfile:\n")
    for code, display in UserProfile.ROLE_CHOICES:
        f.write(f"  {code}: {display}\n")
    f.write("\n")

    # Перевірка користувачів
    f.write("Користувачі в базі даних:\n")
    f.write("-" * 70 + "\n")

    users = User.objects.all()
    for user in users:
        profile = user.profile
        f.write(f"\nКористувач: {user.username}\n")
        f.write(f"  Ім'я: {user.first_name}\n")
        f.write(f"  Прізвище: {user.last_name}\n")
        f.write(f"  Повне ім'я: {user.get_full_name()}\n")
        f.write(f"  Роль (код): {profile.role}\n")
        f.write(f"  Роль (відображення): {profile.get_role_display()}\n")

        # Перевірка байтів
        role_display = profile.get_role_display()
        f.write(f"  Роль (bytes): {role_display.encode('utf-8')}\n")

    f.write("\n" + "=" * 70 + "\n")
    f.write("Перевірку завершено!\n")

print(f"Результати збережено у файл: {output_file}")
print("Відкрийте файл у текстовому редакторі з підтримкою UTF-8 (наприклад, Notepad++, VS Code)")
