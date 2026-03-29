"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from boards import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Si entras a la raíz, vas a la lista de tableros
    path('', lambda r: redirect('board_list')),
    path('boards/', views.board_list, name='board_list'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path('update-task/', views.update_task_position, name='update_task'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # ... anteriores ...
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('export/csv/<int:board_id>/', views.export_tasks_csv, name='export_csv'),
    path('export/json/<int:board_id>/', views.export_tasks_json, name='export_json'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),


]


