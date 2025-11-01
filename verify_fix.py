"""
Перевірка виправлення кодування (виведення у файл)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User

output_file = 'verification_result.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("Результати після виправлення кодування\n")
    f.write("=" * 70 + "\n\n")

    users = User.objects.all()
    for user in users:
        profile = user.profile
        f.write(f"Користувач: {user.username}\n")
        f.write(f"  Повне ім'я: {user.get_full_name()}\n")
        f.write(f"  Роль: {profile.get_role_display()}\n")
        f.write("\n")

    f.write("=" * 70 + "\n")
    f.write("Перевірку завершено!\n")

print(f"Результати збережено у файл: {output_file}")
