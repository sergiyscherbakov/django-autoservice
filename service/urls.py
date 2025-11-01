from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # Client URLs
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('client/car/add/', views.add_car, name='add_car'),
    path('client/order/create/', views.create_order, name='create_order'),

    # Mechanic URLs
    path('mechanic/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('mechanic/order/<int:pk>/update/', views.mechanic_order_update, name='mechanic_order_update'),
    path('mechanic/order/<int:pk>/take/', views.mechanic_take_order, name='mechanic_take_order'),

    # Admin URLs
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/order/<int:pk>/assign/', views.admin_assign_mechanic, name='admin_assign_mechanic'),
    path('admin-panel/order/<int:pk>/edit/', views.admin_order_edit, name='admin_order_edit'),

    # Shared URLs
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]
