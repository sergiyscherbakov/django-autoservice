from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car, Order, UserProfile


class UserRegisterForm(UserCreationForm):
    """Форма реєстрації користувача"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label="Ім'я")
    last_name = forms.CharField(max_length=100, required=True, label='Прізвище')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.phone = self.cleaned_data.get('phone', '')
                user.profile.save()
        return user


class CarForm(forms.ModelForm):
    """Форма додавання/редагування автомобіля"""
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'vin_code', 'license_plate', 'color', 'mileage']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'vin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    """Форма створення замовлення"""
    class Meta:
        model = Order
        fields = ['car', 'service_type', 'description', 'price']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['car'].queryset = Car.objects.filter(owner=user)


class OrderUpdateForm(forms.ModelForm):
    """Форма оновлення замовлення механіком"""
    class Meta:
        model = Order
        fields = ['status', 'mechanic_notes', 'labor_price', 'parts_price', 'price', 'estimated_hours', 'completed_at']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'mechanic_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'labor_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'parts_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class AdminOrderUpdateForm(forms.ModelForm):
    """Форма оновлення замовлення адміністратором"""
    class Meta:
        model = Order
        fields = ['status', 'mechanic', 'labor_price', 'parts_price', 'price', 'estimated_hours', 'mechanic_notes', 'completed_at']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'mechanic': forms.Select(attrs={'class': 'form-control'}),
            'labor_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'parts_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'mechanic_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import UserProfile
        # Обмежити вибір механіків
        self.fields['mechanic'].queryset = User.objects.filter(profile__role='mechanic')


class OrderFilterForm(forms.Form):
    """Форма фільтрації замовлень"""
    status = forms.ChoiceField(
        choices=[('', 'Всі статуси')] + Order.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата з'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата до'
    )
    car_search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номерний знак...'}),
        label='Автомобіль'
    )
    price_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Від...'}),
        label='Ціна від'
    )
    price_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'До...'}),
        label='Ціна до'
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пошук клієнта або опису...'}),
        label='Пошук'
    )
