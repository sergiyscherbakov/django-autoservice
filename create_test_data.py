"""
Скрипт для створення тестових даних
Запуск: python manage.py shell < create_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoservice_project.settings')
django.setup()

from django.contrib.auth.models import User
from service.models import UserProfile, Car, ServiceType, Order
from decimal import Decimal

print("Створення тестових даних...")

# Створення адміністратора
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@autoservice.com',
        password='admin123',
        first_name='Адмін',
        last_name='Адміністратор'
    )
    admin.profile.role = 'admin'
    admin.profile.phone = '+380501234567'
    admin.profile.save()
    print("✓ Створено адміністратора: admin / admin123")

# Створення механіків
mechanics_data = [
    ('mechanic1', 'Іван', 'Петренко', '+380501111111'),
    ('mechanic2', 'Олег', 'Сидоренко', '+380502222222'),
]

for username, first_name, last_name, phone in mechanics_data:
    if not User.objects.filter(username=username).exists():
        mechanic = User.objects.create_user(
            username=username,
            email=f'{username}@autoservice.com',
            password='mechanic123',
            first_name=first_name,
            last_name=last_name
        )
        mechanic.profile.role = 'mechanic'
        mechanic.profile.phone = phone
        mechanic.profile.save()
        print(f"✓ Створено механіка: {username} / mechanic123")

# Створення клієнтів
clients_data = [
    ('client1', 'Марія', 'Коваленко', '+380503333333'),
    ('client2', 'Андрій', 'Шевченко', '+380504444444'),
    ('client3', 'Олена', 'Бондаренко', '+380505555555'),
]

for username, first_name, last_name, phone in clients_data:
    if not User.objects.filter(username=username).exists():
        client = User.objects.create_user(
            username=username,
            email=f'{username}@gmail.com',
            password='client123',
            first_name=first_name,
            last_name=last_name
        )
        client.profile.role = 'client'
        client.profile.phone = phone
        client.profile.save()
        print(f"✓ Створено клієнта: {username} / client123")

# Створення типів послуг
services_data = [
    ('Заміна масла', 'Заміна моторного масла та масляного фільтра', Decimal('800.00')),
    ('Діагностика двигуна', 'Комп\'ютерна діагностика двигуна', Decimal('500.00')),
    ('Заміна гальмівних колодок', 'Заміна передніх або задніх гальмівних колодок', Decimal('1500.00')),
    ('Розвал-сходження', 'Регулювання кутів установки коліс', Decimal('600.00')),
    ('Заміна акумулятора', 'Діагностика та заміна акумулятора', Decimal('2500.00')),
    ('Ремонт підвіски', 'Ремонт елементів підвіски', Decimal('3000.00')),
]

for name, description, price in services_data:
    if not ServiceType.objects.filter(name=name).exists():
        ServiceType.objects.create(
            name=name,
            description=description,
            default_price=price
        )
        print(f"✓ Створено тип послуги: {name}")

# Створення автомобілів для клієнтів
cars_data = [
    ('client1', 'Toyota', 'Camry', 2018, 'JTNB11HK502123456', 'AA1234BB', 'Білий', 85000),
    ('client1', 'Honda', 'Civic', 2020, 'JHMGD38668S123789', 'AA5678CC', 'Сірий', 45000),
    ('client2', 'BMW', 'X5', 2019, 'WBAKF8C53JF123456', 'BB9012DD', 'Чорний', 120000),
    ('client3', 'Volkswagen', 'Passat', 2017, 'WVWZZZ3CZHE123456', 'CC3456EE', 'Синій', 150000),
]

for owner_username, brand, model, year, vin, plate, color, mileage in cars_data:
    owner = User.objects.get(username=owner_username)
    if not Car.objects.filter(vin_code=vin).exists():
        Car.objects.create(
            owner=owner,
            brand=brand,
            model=model,
            year=year,
            vin_code=vin,
            license_plate=plate,
            color=color,
            mileage=mileage
        )
        print(f"✓ Створено автомобіль: {brand} {model} ({plate})")

# Створення замовлень
print("\n✓ Тестові дані успішно створено!")
print("\nОблікові записи для входу:")
print("Адміністратор: admin / admin123")
print("Механіки: mechanic1, mechanic2 / mechanic123")
print("Клієнти: client1, client2, client3 / client123")
