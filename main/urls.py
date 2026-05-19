from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('apply/', views.apply, name='apply'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]