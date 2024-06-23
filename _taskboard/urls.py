from django.urls import path
from . import views

urlpatterns = [
    path('taskboard/', views.taskboard, name="taskboard"),
    path('create-task/', views.create_task, name="create-task"),
    path('delete-task/<str:pk>', views.delete_task, name="delete-task"),
    path('update-task/<str:pk>', views.update_task, name="update-task"),

]