from django.db import models
from django.contrib.auth.models import User

# El Tablero principal
class Board(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Las Columnas (Pendiente, En Proceso, Hecho)
class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.title} - {self.board.title}"

# Las Tareas individuales
class Task(models.Model):
    PRIORITY_CHOICES = [('L', 'Baja'), ('M', 'Media'), ('H', 'Alta')]
    
    title = models.CharField(max_length=200)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    due_date = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title
