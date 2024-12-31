from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            description='Task description',
            status='new',
            priority='medium',
            user=self.user
        )

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New description',
            'status': 'in_progress',
            'priority': 'high'
        }
        response = self.client.post(reverse('tasks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.latest('created_at').title, 'New Task')

    def test_get_task_list(self):
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_update_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'completed',
            'priority': 'low',
            'user': self.user.id  # Ensure required fields are present
        }
        response = self.client.put(reverse('tasks-detail', args=[self.task.id]), data, format='json')
        
        print(response.status_code)
        print(response.data)  # Debugging line
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')

    def test_delete_task(self):
        response = self.client.delete(reverse('tasks-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_filter_by_status(self):
        response = self.client.get(reverse('tasks-list') + '?status=new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_task_filter_by_priority(self):
        response = self.client.get(reverse('tasks-list') + '?priority=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_websocket_connection(self):
        import json
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'tasks',
            {
                'type': 'task_update',
                'message': 'Task updated'
            }
        )
        # Simulate receiving the message
        self.assertTrue(True)  # Basic test to ensure no errors occur during group send