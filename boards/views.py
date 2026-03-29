import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import Board, Column, Task
import csv
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect

from .models import Board, Label # Asegúrate de importar Label

@login_required
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    all_labels = Label.objects.all() # <--- AÑADE ESTA LÍNEA
    return render(request, 'boards/board_detail.html', {
        'board': board,
        'all_labels': all_labels # <--- AÑADE ESTO AL DICCIONARIO
    })


@login_required
def update_task_position(request):
    """ Actualiza la columna de la tarea vía AJAX """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.get(id=data['task_id'])
            new_column = Column.objects.get(id=data['column_id'])
            
            # Verificamos que el usuario sea el dueño del tablero
            if task.column.board.user == request.user:
                task.column = new_column
                task.save()
                return JsonResponse({'status': 'success'})
        except (Task.DoesNotExist, Column.DoesNotExist, KeyError):
            return JsonResponse({'status': 'error'}, status=400)
    
    return JsonResponse({'status': 'invalid method'}, status=405)


@login_required
def board_list(request):
    boards = Board.objects.filter(user=request.user)
    return render(request, 'boards/board_list.html', {'boards': boards})


@login_required
def export_tasks_csv(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{board.title}_tasks.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Tarea', 'Columna', 'Prioridad', 'Fecha Límite'])
    
    for col in board.columns.all():
        for task in col.tasks.all():
            writer.writerow([task.title, col.title, task.get_priority_display(), task.due_date])
    return response

@login_required
def export_tasks_json(request, board_id):
    board = get_object_or_404(Board, id=board_id, user=request.user)
    data = []
    for col in board.columns.all():
        for task in col.tasks.all():
            data.append({
                "title": task.title,
                "column": col.title,
                "priority": task.priority,
                "due_date": str(task.due_date)
            })
    return JsonResponse(data, safe=False)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        column_id = request.POST.get('column_id')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date') or None
        
        column = get_object_or_404(Column, id=column_id)
        
        # Seguridad: Verificar que el tablero pertenece al usuario
        if column.board.user == request.user:
            Task.objects.create(
                column=column,
                title=title,
                priority=priority,
                due_date=due_date
            )
            
    return redirect('board_detail', pk=request.POST.get('board_id'))

@login_required
def delete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        # Seguridad: Solo el dueño del tablero puede borrar
        if task.column.board.user == request.user:
            task.delete()
            return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'error'}, status=400)
