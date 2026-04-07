from django.contrib import admin
from django.urls import path, include
from boards import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- AUTENTICACIÓN ---
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # --- TABLEROS ---
    path('', views.board_list, name='board_list'),
    path('board/<int:pk>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/column/create/', views.create_column, name='create_column'),

    # --- TAREAS ---
    path('task/create/', views.create_task, name='create_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('update-task/', views.update_task_position, name='update_task'),
]
