"""
Показати всіх користувачів з бази даних
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User

output_file = 'users_list.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("Список користувачів в базі даних\n")
    f.write("=" * 70 + "\n\n")

    users = User.objects.all().order_by('id')

    name_header = "Ім'я"
    surname_header = "Прізвище"
    role_header = "Роль"
    f.write(f"{'ID':<5} {'Username':<20} {name_header:<15} {surname_header:<15} {role_header:<15}\n")
    f.write("-" * 70 + "\n")

    for user in users:
        profile = user.profile
        f.write(f"{user.id:<5} {user.username:<20} {user.first_name:<15} {user.last_name:<15} {profile.get_role_display():<15}\n")

    f.write("\n" + "=" * 70 + "\n")
    f.write(f"Всього користувачів: {users.count()}\n")
    f.write("=" * 70 + "\n")

    f.write("\nПАРОЛІ (встановлені скриптом reset_passwords.py):\n")
    f.write("-" * 70 + "\n")
    f.write("admin, mechanic1, mechanic2, client1, client2, client3, sergiy → пароль: 123\n")
    f.write("ivan_petrenko, maria_kovalenko, oleh_shevchenko, anna_bondar,\n")
    f.write("petro_melnyk, vasyl_mechanic, dmytro_master, andriy_technician → пароль: password123\n")
    f.write("admin_user → пароль: admin123\n")

print(f"Список користувачів збережено у файл: {output_file}")
