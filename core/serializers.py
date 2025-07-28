
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import Task, CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        min_length=6
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class StatusValidationMixin:
    """
    Mixin to validate 'status' field across serializers
    """
    VALID_STATUSES = ['New', 'In Progress', 'Completed']

    def validate_status(self, value):
        if value not in self.VALID_STATUSES:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        return value


class TaskSerializer(StatusValidationMixin, serializers.ModelSerializer):
    """
    Serializer for Task CRUD operations
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class TaskCreateSerializer(StatusValidationMixin, serializers.ModelSerializer):
    """
    Serializer for creating tasks
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']


class TaskUpdateSerializer(StatusValidationMixin, serializers.ModelSerializer):
    """
    Serializer for updating tasks
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']