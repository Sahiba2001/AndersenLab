
from core.models import CustomUser, Task
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    """Test user registration"""
    
    def setUp(self):
        self.register_url = reverse('register')
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='johndoe').exists())
    
    def test_user_registration_password_mismatch(self):
        """Test registration with password mismatch"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'testpass123',
            'password_confirm': 'differentpass'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_registration_short_password(self):
        """Test registration with password less than 6 characters"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': '123',
            'password_confirm': '123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskAPITestCase(APITestCase):
    """Test Task API endpoints"""
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )
        
        # Create JWT tokens
        refresh1 = RefreshToken.for_user(self.user1)
        refresh2 = RefreshToken.for_user(self.user2)
        self.token1 = str(refresh1.access_token)
        self.token2 = str(refresh2.access_token)
        
        # URLs
        self.task_list_url = reverse('task-list-create')
        self.task_all_url = reverse('task-list-all')
        
        # Create test tasks
        self.task1 = Task.objects.create(
            title='User1 Task 1',
            description='Description 1',
            status='New',
            user=self.user1
        )
        self.task2 = Task.objects.create(
            title='User1 Task 2',
            description='Description 2',
            status='In Progress',
            user=self.user1
        )
        self.task3 = Task.objects.create(
            title='User2 Task 1',
            description='Description 3',
            status='Completed',
            user=self.user2
        )

    def test_authentication_required(self):
        """Test that authentication is required for task endpoints"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_tasks(self):
        """Test getting all tasks (admin endpoint)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        response = self.client.get(self.task_all_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_user_tasks_only(self):
        """Test that users can only see their own tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verify all tasks belong to user1
        for task in response.data['results']:
            self.assertEqual(task['user'], 'testuser1')

    def test_create_task(self):
        """Test creating a new task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'status': 'New'
        }
        response = self.client.post(self.task_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_create_task_invalid_status(self):
        """Test creating task with invalid status"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'status': 'Invalid Status'
        }
        response = self.client.post(self.task_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task_detail_owner(self):
        """Test getting task detail as owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'User1 Task 1')

    def test_get_task_detail_non_owner(self):
        """Test getting task detail as non-owner (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_owner(self):
        """Test updating task as owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'title': 'Updated Task Title',
            'description': 'Updated description',
            'status': 'In Progress'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task Title')

    def test_update_task_non_owner(self):
        """Test updating task as non-owner (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'title': 'Updated Task Title',
            'status': 'In Progress'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_owner(self):
        """Test deleting task as owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_delete_task_non_owner(self):
        """Test deleting task as non-owner (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_task_completed(self):
        """Test marking task as completed"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        url = reverse('task-complete', args=[self.task1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify task status changed
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'Completed')

    def test_mark_task_completed_non_owner(self):
        """Test marking task as completed by non-owner (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        url = reverse('task-complete', args=[self.task1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        
        # Filter by 'New' status
        response = self.client.get(f'{self.task_list_url}?status=New')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'New')
        
        # Filter by 'In Progress' status
        response = self.client.get(f'{self.task_list_url}?status=In Progress')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'In Progress')

    def test_pagination(self):
        """Test pagination functionality"""
        # Create more tasks to test pagination
        for i in range(15):
            Task.objects.create(
                title=f'Task {i}',
                description=f'Description {i}',
                status='New',
                user=self.user1
            )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination fields
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Should have 10 results per page (PAGE_SIZE = 10)
        self.assertEqual(len(response.data['results']), 10)


class JWTAuthenticationTestCase(APITestCase):
    """Test JWT Authentication"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
    
    def test_obtain_jwt_token(self):
        """Test obtaining JWT token with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_jwt_token_invalid_credentials(self):
        """Test obtaining JWT token with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_jwt_token(self):
        """Test refreshing JWT token"""
        # First, get tokens
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.token_url, data)
        refresh_token = response.data['refresh']
        
        # Now refresh the token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)