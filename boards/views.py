import json
import csv

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .models import Board, Column, Task, Label

# Helper para detectar peticiones AJAX/SPA
def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

# ------------------------
# BOARDS (CRUD HÍBRIDO)
# ------------------------

@login_required
def board_list(request):
    boards = Board.objects.filter(user=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})

@login_required
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    return render(request, 'boards/board_detail.html', {
        'board': board,
        'all_labels': Label.objects.all()
    })

@login_required
@csrf_protect
def create_board(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if not title and request.content_type == 'application/json':
            data = json.loads(request.body)
            title = data.get('title')

        if not title: title = "Nuevo Tablero"
        
        board = Board.objects.create(title=title, user=request.user)
        
        if is_ajax(request):
            return JsonResponse({'status': 'success', 'id': board.id, 'title': board.title})
        return redirect('board_list')
    
    # Soporte para crear vía enlace directo
    Board.objects.create(title="Nuevo Tablero", user=request.user)
    return redirect('board_list')

@login_required
@csrf_protect
def update_board(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            board.title = title
            board.save()
            if is_ajax(request):
                return JsonResponse({'status': 'success', 'title': board.title})
    return redirect('board_list')

@login_required
@csrf_protect
def delete_board(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    if request.method == "POST":
        board.delete()
        if is_ajax(request):
            return JsonResponse({'status': 'success'})
    return redirect('board_list')

# ------------------------
# COLUMNAS (AJAX/SPA)
# ------------------------

@login_required
@csrf_protect
def create_column(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            column = Column.objects.create(board=board, title=title, position=board.columns.count())
            # Forzamos respuesta JSON para evitar redirecciones en el modal
            return JsonResponse({'status': 'success', 'id': column.id, 'title': column.title})
    return JsonResponse({'status': 'error', 'message': 'Título requerido'}, status=400)

@login_required
@csrf_protect
def update_column(request, pk):
    column = get_object_or_404(Column, pk=pk, board__user=request.user)
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            column.title = title
            column.save()
            return JsonResponse({'status': 'success', 'title': column.title})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_protect
def delete_column(request, pk):
    column = get_object_or_404(Column, pk=pk, board__user=request.user)
    if request.method == "POST":
        column.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# ------------------------
# TAREAS
# ------------------------

@login_required
@csrf_protect
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        column_id = request.POST.get('column_id')
        due_date = request.POST.get('due_date') or None
        column = get_object_or_404(Column, id=column_id, board__user=request.user)
        if title:
            task = Task.objects.create(column=column, title=title, due_date=due_date)
            if is_ajax(request):
                return JsonResponse({'status': 'success', 'id': task.id, 'title': task.title})
            return redirect('board_detail', pk=column.board.id)
    return redirect('board_list')

@login_required
@csrf_protect
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, column__board__user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        date = request.POST.get('due_date')
        task.due_date = date if date else None
        task.save()
        if is_ajax(request):
            return JsonResponse({'status': 'updated'})
        return redirect('board_detail', pk=task.column.board.id)
    return redirect('board_list')

@login_required
@csrf_protect
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, column__board__user=request.user)
    board_id = task.column.board.id
    if request.method == 'POST':
        task.delete()
        if is_ajax(request): 
            return JsonResponse({'status': 'deleted'})
        return redirect('board_detail', pk=board_id)
    return redirect('board_list')

@login_required
@csrf_protect
def update_task_position(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.get(id=data['task_id'], column__board__user=request.user)
            new_column = Column.objects.get(id=data['column_id'], board__user=request.user)
            task.column = new_column
            task.save()
            return JsonResponse({'status': 'success'})
        except (json.JSONDecodeError, KeyError, Task.DoesNotExist, Column.DoesNotExist):
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

# ------------------------
# EXPORTACIÓN
# ------------------------

@login_required
def export_tasks_csv(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{board.title}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Tarea', 'Columna', 'Fecha'])
    for col in board.columns.all():
        for t in col.tasks.all():
            writer.writerow([t.title, col.title, t.due_date])
    return response

@login_required
def export_tasks_json(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    data = [{"title": t.title, "column": c.title, "date": str(t.due_date)} 
            for c in board.columns.all() for t in c.tasks.all()]
    return JsonResponse(data, safe=False)

# ------------------------
# AUTENTICACIÓN
# ------------------------

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'