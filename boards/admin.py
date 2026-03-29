from django.contrib import admin
from django.contrib import admin
from .models import Board, Column, Task, Label 

# Register your models here.
from django.contrib import admin
from .models import Board, Column, Task

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'position')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'priority')



@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color') 

