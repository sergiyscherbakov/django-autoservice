from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserProfile(models.Model):
    """Розширення моделі User для ролей користувачів"""
    ROLE_CHOICES = [
        ('client', 'Клієнт'),
        ('mechanic', 'Механік'),
        ('admin', 'Адміністратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'


class Car(models.Model):
    """Модель автомобіля"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Рік випуску')
    vin_code = models.CharField(max_length=17, unique=True, verbose_name='VIN-код')
    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Номерний знак')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Колір')
    mileage = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Пробіг')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'
        ordering = ['-id']


class ServiceType(models.Model):
    """Тип послуги"""
    name = models.CharField(max_length=200, unique=True, verbose_name='Назва послуги')
    description = models.TextField(blank=True, null=True, verbose_name='Опис')
    default_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Стандартна ціна'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип послуги'
        verbose_name_plural = 'Типи послуг'
        ordering = ['name']


class Order(models.Model):
    """Модель замовлення"""
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('in_progress', 'В роботі'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    mechanic = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders',
        limit_choices_to={'profile__role': 'mechanic'}
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(verbose_name='Опис проблеми')

    # Вартість
    labor_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0,
        verbose_name='Вартість роботи'
    )
    parts_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0,
        verbose_name='Вартість деталей'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Загальна вартість'
    )

    # Час виконання
    estimated_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.1'))],
        verbose_name='Очікуваний час виконання (години)'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершення')

    mechanic_notes = models.TextField(blank=True, null=True, verbose_name='Примітки механіка')

    def __str__(self):
        return f"Замовлення #{self.id} - {self.client.username} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']
