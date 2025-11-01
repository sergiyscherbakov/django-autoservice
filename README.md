# Система управління автосервісом

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-4-092E20?style=for-the-badge&logo=django&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

## Автор

**Розробник:** Сергій Щербаков
**Email:** sergiyscherbakov@ukr.net
**Telegram:** @s_help_2010

### 💰 Підтримати розробку
Задонатити на каву USDT (BINANCE SMART CHAIN):
**`0xDFD0A23d2FEd7c1ab8A0F9A4a1F8386832B6f95A`**

---

Веб-додаток для управління автосервісом, розроблений на Django з адаптивним Bootstrap інтерфейсом.

## Функціональність

### Ролі користувачів

1. **Клієнт**
   - Реєстрація та вхід в систему
   - Додавання автомобілів
   - Створення замовлень на ремонт
   - Перегляд історії замовлень
   - Відстеження статусу виконання робіт
   - Перегляд інформації про вартість

2. **Механік**
   - Перегляд доступних замовлень
   - Прийняття замовлень у роботу
   - Оновлення статусу замовлень
   - Додавання приміток до замовлень
   - Редагування вартості робіт

3. **Адміністратор**
   - Управління користувачами
   - Призначення механіків на замовлення
   - Пошук та фільтрація замовлень (за статусом, датою, автомобілем, вартістю)
   - Перегляд статистики
   - Повний доступ до всіх функцій через Django Admin

## Технології

- **Backend:** Python 3.11+ / Django 4.2
- **Frontend:** HTML5 + CSS3 + Bootstrap 5.3
- **База даних:** MySQL 8.0+
- **Іконки:** Bootstrap Icons

## Швидкий старт для розробників

### 1. Клонування репозиторію

```bash
git clone https://github.com/sergiyscherbakov/django-autoservice.git
cd django-autoservice
```

### 2. Створення віртуального середовища

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Застосування міграцій

```bash
python manage.py migrate
```

### 5. Створення суперкористувача

```bash
python manage.py createsuperuser
```

### 6. Створення тестових даних (опціонально)

```bash
python create_test_data.py
```

### 7. Запуск сервера розробки

```bash
python manage.py runserver
```

Додаток буде доступний за адресою: `http://127.0.0.1:8000/`

## Основні команди для розробників

### Міграції бази даних

```bash
# Створити міграції після змін в models.py
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Переглянути SQL команди міграції
python manage.py sqlmigrate service 0001

# Показати статус міграцій
python manage.py showmigrations
```

### Перевірка бази даних

```bash
# Перевірити кодування та структуру БД
python check_db_encoding.py

# Показати всіх користувачів
python show_users.py

# Відкрити Django shell для роботи з БД
python manage.py shell
```

Приклади команд в Django shell:

```python
# Імпорт моделей
from service.models import UserProfile, Car, Order, ServiceType
from django.contrib.auth.models import User

# Перевірка кількості записів
User.objects.count()
UserProfile.objects.count()
Car.objects.count()
Order.objects.count()
ServiceType.objects.count()

# Перегляд всіх користувачів
for user in User.objects.all():
    profile = UserProfile.objects.get(user=user)
    print(f"{user.username} - {profile.get_role_display()}")

# Перегляд замовлень
for order in Order.objects.all():
    print(f"Замовлення #{order.id}: {order.client.username} - {order.status}")

# Створення нового типу послуги
service_type = ServiceType.objects.create(
    name="Заміна масла",
    description="Заміна моторної оливи та фільтра",
    default_price=500.00
)
```

### Управління статичними файлами

```bash
# Збір всіх статичних файлів для продакшену
python manage.py collectstatic

# Очистити та пере-збрати статичні файли
python manage.py collectstatic --clear --noinput
```

### Тестування

```bash
# Запустити всі тести
python manage.py test

# Запустити тести конкретного додатку
python manage.py test service

# Запустити конкретний тест
python manage.py test service.tests.TestOrderModel

# Тести швидкості входу
python test_login_speed.py
python test_login_simple.py
```

### Скрипти для обслуговування

```bash
# Скинути паролі користувачів
python reset_passwords.py

# Виправити кодування даних (якщо потрібно)
python fix_encoding.py
python fix_encoding_auto.py
python fix_names_encoding.py

# Виправити старих користувачів
python fix_old_users.py

# Перевірити виправлення
python verify_fix.py

# Тест відображення
python test_display.py
```

### Перевірка MySQL бази даних

```bash
# Підключитися до MySQL з консолі
mysql -u root -p
# Введіть пароль: 1234

# Після підключення виконайте SQL команди:
USE autoservice;                      # Вибрати базу даних

# Перевірка таблиць та структури
SHOW TABLES;                          # Список всіх таблиць
DESCRIBE auth_user;                   # Структура таблиці користувачів
DESCRIBE service_userprofile;         # Структура таблиці профілів
DESCRIBE service_order;               # Структура таблиці замовлень
DESCRIBE service_car;                 # Структура таблиці автомобілів
DESCRIBE service_servicetype;         # Структура таблиці типів послуг

# Перевірка даних
SELECT * FROM auth_user;              # Всі користувачі
SELECT * FROM service_userprofile;    # Всі профілі
SELECT * FROM service_order LIMIT 10; # Перші 10 замовлень
SELECT * FROM service_car LIMIT 10;   # Перші 10 автомобілів

# Статистика
SELECT COUNT(*) FROM auth_user;       # Кількість користувачів
SELECT COUNT(*) FROM service_order;   # Кількість замовлень
SELECT COUNT(*) FROM service_car;     # Кількість автомобілів

# Перевірка кодування
SHOW VARIABLES LIKE 'character_set%'; # Кодування бази
SHOW VARIABLES LIKE 'collation%';     # Правила сортування

# Замовлення з деталями
SELECT o.id, u.username, c.make, c.model, o.status, o.total_cost
FROM service_order o
JOIN auth_user u ON o.client_id = u.id
JOIN service_car c ON o.car_id = c.id
LIMIT 10;

# Вийти
EXIT;
```

**Альтернативний спосіб - одна команда:**

```bash
# Виконати SQL запит без входу в інтерактивний режим
mysql -u root -p1234 autoservice -e "SHOW TABLES;"
mysql -u root -p1234 autoservice -e "SELECT * FROM auth_user;"
mysql -u root -p1234 autoservice -e "SELECT COUNT(*) as total_users FROM auth_user;"
```

### Django Admin

```bash
# Доступ до панелі адміністратора
http://127.0.0.1:8000/admin/

# Створити суперкористувача
python manage.py createsuperuser

# Змінити пароль користувача
python manage.py changepassword username
```

### Логи та відладка

```bash
# Запустити сервер з детальним виводом
python manage.py runserver --verbosity 3

# Перевірити конфігурацію проєкту
python manage.py check

# Показати налаштування Django
python manage.py diffsettings
```

### Робота з Git

```bash
# Клонувати репозиторій
git clone https://github.com/sergiyscherbakov/django-autoservice.git

# Перевірити статус
git status

# Додати зміни
git add .

# Зробити коміт
git commit -m "Опис змін"

# Відправити зміни
git push origin main

# Отримати зміни
git pull origin main

# Створити нову гілку
git checkout -b feature/new-feature

# Переключитися на гілку
git checkout main
```

## Структура проєкту

```
autoservice/
├── autoservice_project/     # Головний проєкт Django
│   ├── settings.py         # Налаштування
│   ├── urls.py            # Головні URL маршрути
│   └── wsgi.py            # WSGI конфігурація
├── service/               # Головний додаток
│   ├── models.py         # Моделі БД
│   ├── views.py          # Views (логіка)
│   ├── forms.py          # Форми
│   ├── urls.py           # URL маршрути додатку
│   ├── admin.py          # Налаштування Admin панелі
│   ├── signals.py        # Сигнали Django
│   ├── migrations/       # Міграції БД
│   └── templates/        # HTML шаблони
│       ├── service/
│       │   ├── base.html           # Базовий шаблон
│       │   ├── home.html           # Головна сторінка
│       │   ├── order_detail.html   # Деталі замовлення
│       │   ├── client/             # Шаблони клієнта
│       │   ├── mechanic/           # Шаблони механіка
│       │   └── admin/              # Шаблони адміністратора
│       └── registration/           # Шаблони аутентифікації
├── static/               # Статичні файли (CSS, JS, images)
├── media/                # Завантажені файли
├── manage.py             # Django management скрипт
├── requirements.txt      # Python залежності
├── check_db_encoding.py # Перевірка кодування MySQL БД
├── create_test_data.py  # Створення тестових даних
├── show_users.py        # Відображення користувачів
├── reset_passwords.py   # Скидання паролів
├── MYSQL_INFO.md        # Детальна інформація про MySQL
└── README.md            # Документація
```

## Моделі бази даних

### UserProfile
- Розширення User для ролей (клієнт, механік, адміністратор)
- Телефон користувача

### Car (Автомобіль)
- Власник (клієнт)
- Марка, модель, рік випуску
- VIN-код, номерний знак
- Колір, пробіг

### ServiceType (Тип послуги)
- Назва послуги
- Опис
- Стандартна ціна

### Order (Замовлення)
- Клієнт
- Автомобіль
- Механік (призначений)
- Тип послуги
- Статус (очікує, в роботі, виконано, скасовано)
- Опис проблеми
- Вартість
- Дати створення, оновлення, завершення
- Примітки механіка

## URL маршрути

### Загальні
- `/` - Головна сторінка
- `/login/` - Вхід
- `/logout/` - Вихід
- `/register/` - Реєстрація

### Клієнт
- `/client/` - Панель клієнта
- `/client/car/add/` - Додати автомобіль
- `/client/order/create/` - Створити замовлення

### Механік
- `/mechanic/` - Панель механіка
- `/mechanic/order/<id>/update/` - Оновити замовлення
- `/mechanic/order/<id>/take/` - Прийняти замовлення

### Адміністратор
- `/admin-panel/` - Панель адміністратора
- `/admin-panel/order/<id>/assign/` - Призначити механіка
- `/admin/` - Django Admin панель

### Спільні
- `/order/<id>/` - Деталі замовлення

## Налаштування для розробки

### Налаштування MySQL

Проєкт використовує MySQL базу даних. Поточна конфігурація в `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'autoservice',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**Створення бази даних MySQL:**

```bash
# Підключитися до MySQL
mysql -u root -p

# Створити базу даних
CREATE DATABASE autoservice CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Створити користувача (опціонально, якщо не використовуєте root)
CREATE USER 'autoservice_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON autoservice.* TO 'autoservice_user'@'localhost';
FLUSH PRIVILEGES;

# Вийти
EXIT;
```

### Змінні середовища (опціонально)

Можете створити файл `.env` для зберігання чутливих даних:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=autoservice
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=3306
```

Детальну інформацію про роботу з MySQL дивіться в `MYSQL_INFO.md`

## Особливості

- **Адаптивний дизайн** - працює на ПК, планшетах та смартфонах
- **Безпека** - розділення доступу за ролями
- **Зручний інтерфейс** - інтуїтивна навігація
- **Фільтрація та пошук** - швидкий пошук замовлень
- **Статистика** - відображення ключових показників

## Поширені проблеми

### Помилка при запуску сервера

```bash
# Переконайтеся, що віртуальне середовище активоване
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Проблеми з міграціями

```bash
# УВАГА: Це видалить всі дані з БД!
# Підключитися до MySQL та видалити базу
mysql -u root -p -e "DROP DATABASE IF EXISTS autoservice; CREATE DATABASE autoservice CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Видалити файли міграцій (Windows)
del /s service\migrations\0*.py

# Видалити файли міграцій (Linux/Mac)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Створити міграції заново
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Проблеми з кодуванням

```bash
# Запустити скрипт перевірки кодування
python check_db_encoding.py

# Якщо потрібно виправити
python fix_encoding_auto.py
```

## Внесок у проєкт

1. Зробіть форк репозиторію
2. Створіть гілку для нової функції (`git checkout -b feature/AmazingFeature`)
3. Зробіть коміт змін (`git commit -m 'Add some AmazingFeature'`)
4. Відправте зміни (`git push origin feature/AmazingFeature`)
5. Відкрийте Pull Request

## Ліцензія

Цей проєкт створено в навчальних цілях в рамках аспірантури ЗНТУ 124.
