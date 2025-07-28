
from django.urls import path
from .views import (
    TaskListAllView, 
    TaskListCreateView, 
    TaskDetailView, 
    MarkTaskCompletedView, 
    RegisterView,
    UserTasksView
)


urlpatterns = [
    # User registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # Task endpoints
    path('tasks/all/', TaskListAllView.as_view(), name='task-list-all'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/user/', UserTasksView.as_view(), name='user-tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/complete/', MarkTaskCompletedView.as_view(), name='task-complete'),
]
