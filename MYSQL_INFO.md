# Інформація про базу даних MySQL

## ✅ Проєкт успішно переведено на MySQL!

### 📊 Налаштування бази даних

**СУБД:** MySQL 8.0.12
**Назва БД:** `autoservice`
**Користувач:** `root`
**Пароль:** `1234`
**Хост:** `localhost`
**Порт:** `3306`
**Кодування:** `utf8mb4`

---

## 🔍 Команди для перегляду бази даних

### Підключення до MySQL
```bash
mysql -u root -p
# Пароль: 1234
```

### Перегляд всіх баз даних
```bash
mysql -u root -p1234 -e "SHOW DATABASES;"
```

### Вибір бази даних autoservice
```sql
USE autoservice;
```

### Перегляд всіх таблиць
```sql
SHOW TABLES;
```

### Перегляд структури таблиці
```sql
DESCRIBE service_userprofile;
DESCRIBE service_car;
DESCRIBE service_order;
DESCRIBE service_servicetype;
```

---

## 📋 Список таблиць в БД

### Django системні таблиці:
- `auth_group` - групи користувачів
- `auth_group_permissions` - дозволи груп
- `auth_permission` - дозволи
- `auth_user` - користувачі Django
- `auth_user_groups` - зв'язок користувачів та груп
- `auth_user_user_permissions` - дозволи користувачів
- `django_admin_log` - лог дій в адмінці
- `django_content_type` - типи контенту
- `django_migrations` - історія міграцій
- `django_session` - сесії користувачів

### Таблиці додатку:
- `service_userprofile` - профілі користувачів (ролі)
- `service_car` - автомобілі
- `service_order` - замовлення
- `service_servicetype` - типи послуг

---

## 📊 Запити для перегляду даних

### Переглянути всіх користувачів
```sql
USE autoservice;
SELECT id, username, email, first_name, last_name, is_staff, is_active
FROM auth_user;
```

### Переглянути профілі користувачів з ролями
```sql
SELECT
    u.username,
    u.first_name,
    u.last_name,
    p.role,
    p.phone
FROM auth_user u
LEFT JOIN service_userprofile p ON u.id = p.user_id;
```

### Переглянути всі автомобілі
```sql
SELECT
    c.id,
    c.brand,
    c.model,
    c.year,
    c.license_plate,
    c.vin_code,
    u.username as owner
FROM service_car c
JOIN auth_user u ON c.owner_id = u.id;
```

### Переглянути всі типи послуг
```sql
SELECT id, name, description, default_price
FROM service_servicetype;
```

### Переглянути всі замовлення
```sql
SELECT
    o.id,
    client.username as client,
    mechanic.username as mechanic,
    c.license_plate as car,
    st.name as service,
    o.status,
    o.price,
    o.created_at
FROM service_order o
JOIN auth_user client ON o.client_id = client.id
LEFT JOIN auth_user mechanic ON o.mechanic_id = mechanic.id
JOIN service_car c ON o.car_id = c.id
JOIN service_servicetype st ON o.service_type_id = st.id
ORDER BY o.created_at DESC;
```

### Статистика по статусам замовлень
```sql
SELECT
    status,
    COUNT(*) as count
FROM service_order
GROUP BY status;
```

---

## 🔧 Корисні команди Django

### Відкрити Django shell з доступом до БД
```bash
python manage.py dbshell
```

### Переглянути SQL запити міграцій
```bash
python manage.py sqlmigrate service 0001
```

### Перевірити підключення до БД
```bash
python manage.py check --database default
```

---

## 📈 Поточні дані в БД

**Користувачі:** 6
- 1 адміністратор (admin)
- 2 механіки (mechanic1, mechanic2)
- 3 клієнти (client1, client2, client3)

**Автомобілі:** 4
- Toyota Camry 2018
- Honda Civic 2020
- BMW X5 2019
- Volkswagen Passat 2017

**Типи послуг:** 6
- Заміна масла (800 грн)
- Діагностика двигуна (500 грн)
- Заміна гальмівних колодок (1500 грн)
- Розвал-сходження (600 грн)
- Заміна акумулятора (2500 грн)
- Ремонт підвіски (3000 грн)

**Замовлення:** 0 (нові можна створити через веб-інтерфейс)

---

## 🔐 Безпека

⚠️ **ВАЖЛИВО:** У продакшн середовищі:
1. Змініть пароль бази даних
2. Створіть окремого користувача БД (не root)
3. Використовуйте змінні середовища для зберігання паролів
4. Налаштуйте правильні права доступу

---

## 💾 Резервне копіювання

### Створити backup бази даних
```bash
mysqldump -u root -p1234 autoservice > backup_autoservice.sql
```

### Відновити з backup
```bash
mysql -u root -p1234 autoservice < backup_autoservice.sql
```

---

## 🔄 Міграції

Всі міграції успішно застосовані до MySQL бази даних.

Для перегляду списку міграцій:
```bash
python manage.py showmigrations
```

---

**База даних готова до використання!** ✅

Сервер запущено на: http://127.0.0.1:8000/
