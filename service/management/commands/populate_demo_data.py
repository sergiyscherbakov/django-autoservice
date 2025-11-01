from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from service.models import UserProfile, Car, ServiceType, Order
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Створення демонстраційних даних...')

        # Створення користувачів
        self.stdout.write('Створення користувачів...')

        # Клієнти
        clients = []
        client_data = [
            ('ivan_petrenko', 'Іван', 'Петренко', 'ivan@example.com', '+380501234567'),
            ('maria_kovalenko', 'Марія', 'Коваленко', 'maria@example.com', '+380502345678'),
            ('oleh_shevchenko', 'Олег', 'Шевченко', 'oleh@example.com', '+380503456789'),
            ('anna_bondar', 'Анна', 'Бондар', 'anna@example.com', '+380504567890'),
            ('petro_melnyk', 'Петро', 'Мельник', 'petro@example.com', '+380505678901'),
        ]

        for username, first_name, last_name, email, phone in client_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            if created:
                user.set_password('client123')
                user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'client', 'phone': phone}
            )
            clients.append(user)

        self.stdout.write(f'[OK] Створено {len(clients)} клієнтів')

        # Механіки
        mechanics = []
        mechanic_data = [
            ('vasyl_mechanic', 'Василь', 'Механік', 'vasyl@autoservice.com', '+380506789012'),
            ('dmytro_master', 'Дмитро', 'Майстер', 'dmytro@autoservice.com', '+380507890123'),
            ('andriy_technician', 'Андрій', 'Технік', 'andriy@autoservice.com', '+380508901234'),
        ]

        for username, first_name, last_name, email, phone in mechanic_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            if created:
                user.set_password('mechanic123')
                user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'mechanic', 'phone': phone}
            )
            mechanics.append(user)

        self.stdout.write(f'[OK] Створено {len(mechanics)} механіків')

        # Адміністратори
        admin_user, created = User.objects.get_or_create(
            username='admin_user',
            defaults={
                'first_name': 'Сергій',
                'last_name': 'Адміністратор',
                'email': 'admin@autoservice.com',
                'is_staff': False,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'admin', 'phone': '+380509012345'}
        )
        self.stdout.write('[OK] Створено адміністратора')

        # Створення автомобілів
        self.stdout.write('Створення автомобілів...')
        cars_data = [
            # Іван Петренко
            ('Toyota', 'Camry', 2018, 'АА1234ВВ', 'ABC1234567890IVAN', 'Білий', 85000),
            # Марія Коваленко
            ('Honda', 'Civic', 2020, 'ВВ5678СС', 'XYZ9876543210MARI', 'Чорний', 42000),
            ('BMW', 'X5', 2019, 'СС9012DD', 'BMW1234567890MARI', 'Сірий', 67000),
            # Олег Шевченко
            ('Mercedes', 'E-Class', 2017, 'DD3456EE', 'MERC98765432OLEH', 'Синій', 125000),
            # Анна Бондар
            ('Volkswagen', 'Passat', 2021, 'EE7890FF', 'VW12345678901ANNA', 'Червоний', 28000),
            # Петро Мельник
            ('Audi', 'A4', 2016, 'FF1122GG', 'AUDI87654321PETR', 'Зелений', 156000),
            ('Skoda', 'Octavia', 2022, 'GG3344HH', 'SKODA1234567PETR', 'Сірий', 15000),
        ]

        cars = []
        client_cars = {client: [] for client in clients}

        for i, (brand, model, year, plate, vin, color, mileage) in enumerate(cars_data):
            client = clients[i % len(clients)]
            car, created = Car.objects.get_or_create(
                vin_code=vin,
                defaults={
                    'owner': client,
                    'brand': brand,
                    'model': model,
                    'year': year,
                    'license_plate': plate,
                    'color': color,
                    'mileage': mileage,
                }
            )
            cars.append(car)
            client_cars[client].append(car)

        self.stdout.write(f'[OK] Створено {len(cars)} автомобілів')

        # Створення типів послуг
        self.stdout.write('Створення типів послуг...')
        service_types_data = [
            ('Заміна масла', 'Заміна моторного масла та масляного фільтра', 800),
            ('Діагностика двигуна', 'Комп\'ютерна діагностика двигуна', 500),
            ('Ремонт підвіски', 'Ремонт та заміна елементів підвіски', 2500),
            ('Заміна гальмівних колодок', 'Заміна передніх та задніх гальмівних колодок', 1200),
            ('Розвал-сход', 'Регулювання кутів установки коліс', 600),
            ('Заміна свічок запалювання', 'Заміна комплекту свічок запалювання', 400),
            ('Ремонт коробки передач', 'Діагностика та ремонт КПП', 5000),
            ('Заміна ременя ГРМ', 'Заміна ременя газорозподільного механізму', 3500),
            ('Кондиціонування', 'Заправка та обслуговування кондиціонера', 1000),
            ('Заміна акумулятора', 'Заміна акумуляторної батареї', 2000),
            ('Полірування кузова', 'Професійне полірування автомобіля', 1800),
            ('Шиномонтаж', 'Заміна та балансування коліс', 300),
        ]

        service_types = []
        for name, description, price in service_types_data:
            service_type, _ = ServiceType.objects.get_or_create(
                name=name,
                defaults={'description': description, 'default_price': price}
            )
            service_types.append(service_type)

        self.stdout.write(f'[OK] Створено {len(service_types)} типів послуг')

        # Створення замовлень
        self.stdout.write('Створення замовлень...')

        statuses = ['pending', 'in_progress', 'completed', 'cancelled']

        descriptions = [
            'Потрібна термінова заміна, автомобіль використовується щодня',
            'Виявлено проблему під час їзди, необхідна діагностика',
            'Планове обслуговування згідно з регламентом',
            'Після зими потрібне відновлення',
            'Виникли дивні звуки, потрібна перевірка',
            'Рекомендація від попереднього ТО',
            'Горить лампочка на панелі приладів',
            'Втрата потужності двигуна',
            'Вібрація при гальмуванні',
            'Перед дальньою поїздкою',
        ]

        mechanic_notes_variants = [
            'Виконано заміну відповідно до регламенту. Використано оригінальні запчастини.',
            'Виявлено додаткові проблеми, рекомендую профілактичний огляд через місяць.',
            'Роботу виконано успішно. Автомобіль готовий до експлуатації.',
            'Встановлено нові компоненти. Гарантія 12 місяців або 20000 км.',
            'Усі системи працюють нормально. Рекомендую наступне ТО через 10000 км.',
        ]

        orders_count = 30
        for i in range(orders_count):
            client = random.choice(clients)
            car = random.choice(client_cars[client]) if client_cars[client] else random.choice(cars)
            service_type = random.choice(service_types)
            status = random.choice(statuses)

            # Генерація дат
            days_ago = random.randint(0, 60)
            created_at = timezone.now() - timedelta(days=days_ago)

            order_data = {
                'client': client,
                'car': car,
                'service_type': service_type,
                'status': status,
                'description': random.choice(descriptions),
                'price': service_type.default_price + random.randint(-200, 500),
                'created_at': created_at,
            }

            # Призначення механіка для активних та завершених замовлень
            if status in ['in_progress', 'completed']:
                order_data['mechanic'] = random.choice(mechanics)
                order_data['mechanic_notes'] = random.choice(mechanic_notes_variants) if random.random() > 0.3 else ''

            # Дата завершення для виконаних замовлень
            if status == 'completed':
                completion_days = random.randint(1, 5)
                order_data['completed_at'] = created_at + timedelta(days=completion_days)

            order = Order.objects.create(**order_data)

        self.stdout.write(f'[OK] Створено {orders_count} замовлень')

        self.stdout.write(self.style.SUCCESS('\n[OK] Демонстраційні дані успішно створено!'))
        self.stdout.write('\nОблікові дані:')
        self.stdout.write('Клієнти: ivan_petrenko, maria_kovalenko, oleh_shevchenko, anna_bondar, petro_melnyk (пароль: client123)')
        self.stdout.write('Механіки: vasyl_mechanic, dmytro_master, andriy_technician (пароль: mechanic123)')
        self.stdout.write('Адміністратор: admin_user (пароль: admin123)')
