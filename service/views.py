from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Order, Car, ServiceType, UserProfile
from .forms import UserRegisterForm, CarForm, OrderForm, OrderUpdateForm, OrderFilterForm, AdminOrderUpdateForm


def is_admin(user):
    """Перевірка чи є користувач адміністратором"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin'


def is_mechanic(user):
    """Перевірка чи є користувач механіком"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'mechanic'


def is_client(user):
    """Перевірка чи є користувач клієнтом"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'client'


def home(request):
    """Головна сторінка"""
    return render(request, 'service/home.html')


def register(request):
    """Реєстрація нового користувача"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрацію успішно завершено!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# === Панель клієнта ===

@login_required
@user_passes_test(is_client, login_url='home')
def client_dashboard(request):
    """Панель клієнта"""
    from django.db.models import Sum, Count

    orders = Order.objects.filter(client=request.user).order_by('-created_at')
    cars = Car.objects.filter(owner=request.user)

    # Статистика клієнта
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    in_progress_orders = orders.filter(status='in_progress').count()
    completed_orders = orders.filter(status='completed').count()

    # Загальна сума витрат
    total_spent = orders.filter(status='completed').aggregate(Sum('price'))['price__sum'] or 0

    # Останні замовлення (топ-5)
    recent_orders = orders[:5]

    stats = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'total_spent': total_spent,
        'total_cars': cars.count(),
    }

    return render(request, 'service/client/dashboard.html', {
        'orders': recent_orders,
        'all_orders': orders,
        'cars': cars,
        'stats': stats,
    })


@login_required
@user_passes_test(is_client, login_url='home')
def add_car(request):
    """Додавання автомобіля"""
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, 'Автомобіль успішно додано!')
            return redirect('client_dashboard')
    else:
        form = CarForm()
    return render(request, 'service/client/car_form.html', {'form': form})


@login_required
@user_passes_test(is_client, login_url='home')
def create_order(request):
    """Створення нового замовлення"""
    if request.method == 'POST':
        form = OrderForm(request.user, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            messages.success(request, 'Замовлення успішно створено!')
            return redirect('client_dashboard')
    else:
        form = OrderForm(user=request.user)
    return render(request, 'service/client/order_form.html', {'form': form})


@login_required
def order_detail(request, pk):
    """Деталі замовлення"""
    order = get_object_or_404(Order, pk=pk)

    # Перевірка прав доступу
    if not (order.client == request.user or
            order.mechanic == request.user or
            is_admin(request.user)):
        messages.error(request, 'У вас немає доступу до цього замовлення')
        return redirect('home')

    return render(request, 'service/order_detail.html', {'order': order})


# === Панель механіка ===

@login_required
@user_passes_test(is_mechanic, login_url='home')
def mechanic_dashboard(request):
    """Панель механіка"""
    from django.db.models import Sum, Count

    orders = Order.objects.filter(mechanic=request.user).order_by('-created_at')
    pending_orders = Order.objects.filter(status='pending').order_by('-created_at')

    # Статистика механіка
    total_orders = orders.count()
    in_progress_orders = orders.filter(status='in_progress').count()
    completed_orders = orders.filter(status='completed').count()

    # Дохід від виконаних робіт
    total_earned = orders.filter(status='completed').aggregate(Sum('price'))['price__sum'] or 0

    stats = {
        'total_orders': total_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'pending_available': pending_orders.count(),
        'total_earned': total_earned,
    }

    return render(request, 'service/mechanic/dashboard.html', {
        'orders': orders,
        'pending_orders': pending_orders,
        'stats': stats,
    })


@login_required
@user_passes_test(is_mechanic, login_url='home')
def mechanic_order_update(request, pk):
    """Оновлення замовлення механіком"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            if order.status == 'completed' and not order.completed_at:
                order.completed_at = timezone.now()
            order.save()
            messages.success(request, 'Замовлення оновлено!')
            return redirect('mechanic_dashboard')
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'service/mechanic/order_update.html', {
        'form': form,
        'order': order,
    })


@login_required
@user_passes_test(is_mechanic, login_url='home')
def mechanic_take_order(request, pk):
    """Прийняття замовлення механіком"""
    order = get_object_or_404(Order, pk=pk, status='pending')
    order.mechanic = request.user
    order.status = 'in_progress'
    order.save()
    messages.success(request, 'Ви прийняли замовлення!')
    return redirect('mechanic_dashboard')


# === Панель адміністратора ===

@login_required
@user_passes_test(is_admin, login_url='home')
def admin_dashboard(request):
    """Панель адміністратора"""
    from django.db.models import Sum, Count, Avg
    from datetime import datetime, timedelta

    # Фільтрація
    filter_form = OrderFilterForm(request.GET)
    orders = Order.objects.all().select_related('client', 'car', 'mechanic', 'service_type')

    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        car_search = filter_form.cleaned_data.get('car_search')
        price_min = filter_form.cleaned_data.get('price_min')
        price_max = filter_form.cleaned_data.get('price_max')
        search = filter_form.cleaned_data.get('search')

        if status:
            orders = orders.filter(status=status)
        if date_from:
            orders = orders.filter(created_at__gte=date_from)
        if date_to:
            orders = orders.filter(created_at__lte=date_to)
        if car_search:
            orders = orders.filter(car__license_plate__icontains=car_search)
        if price_min:
            orders = orders.filter(price__gte=price_min)
        if price_max:
            orders = orders.filter(price__lte=price_max)
        if search:
            orders = orders.filter(
                Q(client__username__icontains=search) |
                Q(client__first_name__icontains=search) |
                Q(client__last_name__icontains=search) |
                Q(description__icontains=search)
            )

    orders = orders.order_by('-created_at')

    # Статистика
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    in_progress_orders = Order.objects.filter(status='in_progress').count()
    completed_orders = Order.objects.filter(status='completed').count()

    # Додаткова статистика
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('price'))['price__sum'] or 0
    avg_order_price = Order.objects.aggregate(Avg('price'))['price__avg'] or 0

    # Статистика за останні 30 днів
    last_30_days = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=last_30_days).count()
    recent_revenue = Order.objects.filter(
        created_at__gte=last_30_days,
        status='completed'
    ).aggregate(Sum('price'))['price__sum'] or 0

    # Топ послуги
    top_services = ServiceType.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count')[:5]

    # Активність механіків
    mechanics_stats = UserProfile.objects.filter(role='mechanic').annotate(
        total_orders=Count('user__assigned_orders'),
        completed_orders=Count('user__assigned_orders', filter=Q(user__assigned_orders__status='completed'))
    ).select_related('user')

    stats = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'avg_order_price': avg_order_price,
        'recent_orders': recent_orders,
        'recent_revenue': recent_revenue,
        'top_services': top_services,
        'mechanics_stats': mechanics_stats,
    }

    return render(request, 'service/admin/dashboard.html', {
        'orders': orders,
        'filter_form': filter_form,
        'stats': stats,
    })


@login_required
@user_passes_test(is_admin, login_url='home')
def admin_assign_mechanic(request, pk):
    """Призначення механіка на замовлення"""
    order = get_object_or_404(Order, pk=pk)
    mechanics = UserProfile.objects.filter(role='mechanic').select_related('user')

    if request.method == 'POST':
        mechanic_id = request.POST.get('mechanic_id')
        if mechanic_id:
            mechanic = get_object_or_404(UserProfile, id=mechanic_id, role='mechanic')
            order.mechanic = mechanic.user
            order.status = 'in_progress'
            order.save()
            messages.success(request, f'Механіка {mechanic.user.username} призначено на замовлення!')
            return redirect('admin_dashboard')

    return render(request, 'service/admin/assign_mechanic.html', {
        'order': order,
        'mechanics': mechanics,
    })


@login_required
@user_passes_test(is_admin, login_url='home')
def admin_order_edit(request, pk):
    """Редагування замовлення адміністратором"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = AdminOrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            if order.status == 'completed' and not order.completed_at:
                order.completed_at = timezone.now()
            order.save()
            messages.success(request, 'Замовлення успішно оновлено!')
            return redirect('admin_dashboard')
    else:
        form = AdminOrderUpdateForm(instance=order)

    return render(request, 'service/admin/order_edit.html', {
        'form': form,
        'order': order,
    })
