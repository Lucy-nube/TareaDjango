from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


class Label(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#3b82f6") # Color Hexadecimal

    def __str__(self):  
        return self.name



class Board(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título del Tablero")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Column(models.Model):
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Nombre de la Columna")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.title} - {self.board.title}"

class Task(models.Model):
    PRIORITY_CHOICES = [('L', 'Baja'), ('M', 'Media'), ('H', 'Alta')]
    
    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Tarea")
    labels = models.ManyToManyField(Label, blank=True)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Asignada a")
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title



@receiver(post_save, sender=Task)
def notify_assignment(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        send_mail(
            'Nueva Tarea Asignada',
            f'Hola, se te ha asignado la tarea: {instance.title}',
            'noreply@gestorpro.com',
            [instance.assigned_to.email],
            fail_silently=True,
        )

