from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from core.models import CustomUser, Task
from rest_framework import status
from django.test import TestCase


class TestTaskAPI(APITestCase):  # Use APITestCase for DRF support

    def setUp(self):
        # Create two users
        self.user = CustomUser.objects.create_user(username='user1', password='password123')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password123')

        # JWT login
        self.login_url = reverse('token_obtain_pair')
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'password123'
        })
        self.access_token = response.data['access']
        self.auth_header = f'Bearer {self.access_token}'

        # Your task URL (ensure 'task-list-create' is correct)
        self.task_url = reverse('task-list-create')

    def test_user_can_create_task(self):
        data = {"title": "Test Task"}
        response = self.client.post(
            self.task_url,
            data,
            format='json',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_list_own_tasks(self):
        Task.objects.create(title='T1', user=self.user)
        Task.objects.create(title='T2', user=self.user2)

        response = self.client.get(self.task_url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'T1')

    def test_user_cannot_access_other_users_task_detail(self):
        task = Task.objects.create(title='Other Task', user=self.user2)
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_mark_task_as_completed(self):
        task = Task.objects.create(title='To Complete', user=self.user)
        url = reverse('task-complete', args=[task.id])
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')

    def test_user_can_filter_tasks_by_status(self):
        Task.objects.create(title='T1', status='new', user=self.user)
        Task.objects.create(title='T2', status='completed', user=self.user)

        response = self.client.get(
            self.task_url + '?status=completed',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'completed')

    def test_auth_required_for_tasks(self):
        response = self.client.get(self.task_url)  # no auth
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
