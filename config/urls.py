from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls), 

    # -------------------
    # AUTH
    # -------------------
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # -------------------
    # HOME (Redirige al listado de tableros)
    # -------------------
    path('', lambda r: redirect('board_list')),
    # -------------------
    # BOARDS (CRUD COMPLETO)
    # -------------------
    path('boards/', views.board_list, name='board_list'),
    path('boards/create/', views.create_board, name='create_board'),
    path('boards/<int:pk>/', views.board_detail, name='board_detail'),
    path('boards/update/<int:pk>/', views.update_board, name='update_board'), # Corregido para AJAX
    path('boards/delete/<int:pk>/', views.delete_board, name='delete_board'), # Corregido para AJAX

    # -------------------
    # COLUMNAS (CRUD AJAX)
    # -------------------
    path('boards/<int:board_id>/columns/create/', views.create_column, name='create_column'),
    path('columns/update/<int:pk>/', views.update_column, name='update_column'),
    path('columns/delete/<int:pk>/', views.delete_column, name='delete_column'),

    # -------------------
    # TASKS (Manejo de fecha corregido)
    # -------------------
    path('task/create/', views.create_task, name='create_task'), # Lógica para evitar error de fecha
    path('task/update/<int:pk>/', views.update_task, name='update_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('task/update-position/', views.update_task_position, name='update_task_position'),

    # -------------------
    # EXPORTS
    # -------------------
    path('export/csv/<int:board_id>/', views.export_tasks_csv, name='export_tasks_csv'), # Nombre unificado[cite: 2]
    path('export/json/<int:board_id>/', views.export_tasks_json, name='export_tasks_json'), # Nombre unificado[cite: 2]
]