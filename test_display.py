"""
Тест відображення ролей
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User
from service.models import UserProfile

# Отримати адміністратора
admin_user = User.objects.filter(profile__role='admin').first()

if admin_user:
    profile = admin_user.profile

    print("Інформація про користувача:")
    print(f"Username: {admin_user.username}")
    print(f"Повне ім'я: {admin_user.get_full_name()}")
    print(f"Роль (code): {profile.role}")
    print(f"Роль (display): {profile.get_role_display()}")
    print()
    print(f"ROLE_CHOICES з моделі: {UserProfile.ROLE_CHOICES}")
    print()

    # Перевірка в HTML
    html_output = f"""
    В шаблоні буде:
    <h5>Вітаємо, {admin_user.get_full_name()}</h5>
    <p>Роль: {profile.get_role_display()}</p>
    """
    print(html_output)
else:
    print("Адміністратора не знайдено!")
