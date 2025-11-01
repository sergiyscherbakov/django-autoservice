from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Car, ServiceType, Order


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профіль'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')

    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else '-'
    get_role.short_description = 'Роль'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'year', 'owner', 'mileage')
    list_filter = ('brand', 'year')
    search_fields = ('license_plate', 'vin_code', 'brand', 'model', 'owner__username')
    readonly_fields = ('id',)


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_price')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'car', 'service_type', 'status', 'mechanic', 'price', 'estimated_hours', 'created_at')
    list_filter = ('status', 'created_at', 'service_type')
    search_fields = ('client__username', 'car__license_plate', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основна інформація', {
            'fields': ('client', 'car', 'service_type', 'status', 'mechanic')
        }),
        ('Деталі замовлення', {
            'fields': ('description', 'mechanic_notes')
        }),
        ('Вартість', {
            'fields': ('labor_price', 'parts_price', 'price', 'estimated_hours')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


# Перереєстрація User моделі з профілем
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
