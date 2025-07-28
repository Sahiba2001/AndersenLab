
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Task, CustomUser
from .serializers import (
    TaskSerializer, 
    TaskCreateSerializer, 
    TaskUpdateSerializer, 
    UserRegisterSerializer, 
    UserSerializer
)



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


class TaskFilterMixin:
    """
    Mixin for adding filtering and ordering to task views
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class TaskListAllView(TaskFilterMixin, generics.ListAPIView):
    """
    Get a list of all tasks (for admin purposes)
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskListCreateView(TaskFilterMixin, generics.ListCreateAPIView):
    """
    Get a list of all user's tasks and create new tasks
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return tasks for the current user only"""
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        """Save the task with the current user"""
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get information about a specific task, update and delete tasks
    Only the owner can update/delete their tasks
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Return tasks for the current user only"""
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskSerializer
    

class MarkTaskCompletedView(APIView):
    """
    Mark a task as completed
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.status = 'Completed'
        task.save()
        
        serializer = TaskSerializer(task)
        return Response({
            'message': 'Task marked as completed.',
            'task': serializer.data
        }, status=status.HTTP_200_OK)
    

class UserTasksView(generics.ListAPIView):
    """
    Get a list of all user's tasks (alternative endpoint)
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return tasks for the current user only"""
        return Task.objects.filter(user=self.request.user)