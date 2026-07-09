from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='index'),
    path('create/', views.task_create, name='create_task'),
    path('complete/<int:id>/', views.task_complete, name='complete_task'),
    path('view/<int:id>/', views.task_list, name='view_task'), 
    path('edit/<int:id>/', views.task_edit, name='edit_task'),
    path('delete/<int:id>/', views.task_delete, name='delete_task'),
]