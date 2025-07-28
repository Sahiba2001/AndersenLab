
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Custom User model with required fields as per task requirements
    """
    first_name = models.CharField(max_length=150, verbose_name="First Name")
    last_name = models.TextField(blank=True, null=True, verbose_name="Last Name")
    username = models.CharField(max_length=150, unique=True, verbose_name="Username")
    password = models.CharField(
        max_length=128, 
        validators=[MinLengthValidator(6)],
        verbose_name="Password"
    )

    # Override required fields to match task requirements
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Task(models.Model):
    """
    Task model with all required fields as per task requirements
    """
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='New',
        verbose_name="Status"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="User"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} - {self.user.username}"