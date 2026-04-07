import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from .models import Board, Column, Task

# --- VISTA DE REGISTRO ---
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- LISTADO DE TABLEROS (Página Principal) ---
@login_required
def board_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Board.objects.create(title=title, user=request.user)
        return redirect('board_list')
    
    boards = request.user.boards.all()
    # Si index.html está fuera de la carpeta boards, déjalo así. 
    # Si está dentro, cámbialo a 'boards/index.html'
    return render(request, 'index.html', {'boards': boards})

# --- DETALLE DEL TABLERO (Vista Kanban) ---
@login_required
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    columns = board.columns.prefetch_related('tasks').all()
    # CAMBIO: Ahora apunta a boards/board_detail.html
    return render(request, 'boards/board_detail.html', {'board': board, 'columns': columns})

# --- COLUMNAS ---
@login_required
def create_column(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Column.objects.create(board=board, title=title)
    return redirect('board_detail', pk=board_id)

# --- TAREAS ---
@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        column_id = request.POST.get('column_id')
        board_id = request.POST.get('board_id')
        
        column = get_object_or_404(Column, id=column_id, board__user=request.user)
        if title:
            Task.objects.create(title=title, column=column)
            
        return redirect('board_detail', pk=board_id)
    return redirect('board_list')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, column__board__user=request.user)
    board_id = task.column.board.id
    task.delete()
    return redirect('board_detail', pk=board_id)

@login_required
def update_task_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=data.get('task_id'), column__board__user=request.user)
        new_column = get_object_or_404(Column, id=data.get('column_id'), board__user=request.user)
        task.column = new_column
        task.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
