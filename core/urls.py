
from django.urls import path, include
from .views import TaskListAllView, TaskListCreateView, TaskDetailView, MarkTaskCompletedView, RegisterView


urlpatterns = [
    path('tasks/all/', TaskListAllView.as_view(), name='task-list-all'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', MarkTaskCompletedView.as_view(), name='task-complete'),
    path('register/', RegisterView.as_view(), name='register'),
]
