from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils import timezone

# ------------------------
# LABEL (ETIQUETAS)
# ------------------------
class Label(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    color = models.CharField(max_length=7, default="#3b82f6", verbose_name="Color Hex")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"


# ------------------------
# BOARD (TABLERO)
# ------------------------
class Board(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título del Tablero")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"


# ------------------------
# COLUMN (COLUMNA)
# ------------------------
class Column(models.Model):
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Nombre de Columna")
    position = models.PositiveIntegerField(default=0, verbose_name="Posición")

    class Meta:
        ordering = ['position']
        verbose_name = "Columna"
        verbose_name_plural = "Columnas"

    def __str__(self):
        return f"{self.title} ({self.board.title})"


# ------------------------
# TASK (TAREA) - CORREGIDO SEGÚN REQUERIMIENTOS
# ------------------------
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Baja'),
        ('M', 'Media'),
        ('H', 'Alta')
    ]

    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Título de la Tarea")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    # Relaciones
    labels = models.ManyToManyField(Label, blank=True, verbose_name="Etiquetas")
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Asignado a"
    )

    # Atributos
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M', verbose_name="Prioridad")
    position = models.PositiveIntegerField(default=0, verbose_name="Orden")
    
    # CORRECCIÓN CRÍTICA: Campo de fecha límite solicitado por el profesor
    due_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Fecha Límite"
    )

    class Meta:
        ordering = ['position']
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"

    def __str__(self):
        return self.title

    def clean(self):
        """Validación de fecha para evitar fechas pasadas"""
        super().clean()
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError({'due_date': "La fecha límite no puede estar en el pasado."})


# ------------------------
# SIGNALS (NOTIFICACIONES)
# ------------------------
@receiver(post_save, sender=Task)
def notify_assignment(sender, instance, created, **kwargs):
    """Envía un correo cuando se crea una tarea y tiene un usuario asignado"""
    if created and instance.assigned_to and instance.assigned_to.email:
        subject = f'Nueva Tarea: {instance.title}'
        message = f'Hola {instance.assigned_to.username},\n\nSe te ha asignado una nueva tarea en el tablero: "{instance.title}".\nPrioridad: {instance.get_priority_display()}'
        
        send_mail(
            subject,
            message,
            'noreply@gestorpro.com',
            [instance.assigned_to.email],
            fail_silently=True,
        )