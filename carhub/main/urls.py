from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('car_list/', views.car_list, name='car_list'),
    # path('car_detail/<int:pk>/', views.car_detail, name='car_detail'),
    path('dealer_list/', views.dealer_list, name='dealer_list'),
    path('dealer_detail/<int:pk>/', views.dealer_detail, name='dealer_detail'),
    path('add_car/', views.add_car, name='add_car'),
    path('car_detail/<int:car_id>/', views.car_detail, name='car_detail'),
    path('add_to_wishlist/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('manage_cars/', views.manage_cars, name='manage_cars'),
    path('update_car/<int:pk>/', views.update_car, name='update_car'),
    path('delete_car/<int:pk>/', views.delete_car, name='delete_car'),
    path('update_profile/', views.update_profile, name='update_profile'),
]
