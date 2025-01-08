from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
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
        cache.clear()  # Clear cache before each test

    def tearDown(self):
        cache.clear()  # Clear cache after each test to avoid persistence

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New description',
            'status': 'in_progress',
            'priority': 'high'
        }
        # First call - populates cache
        response = self.client.post(reverse('tasks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

        # Check cache invalidation
        cached_data = cache.get('tasks:')
        self.assertIsNone(cached_data)  # Cache should be invalidated

    def test_get_task_list(self):
        # Call task list twice to check cache population
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Check if response is cached
        cached_data = cache.get(f"tasks:{response.wsgi_request.GET.urlencode()}")
        self.assertIsNotNone(cached_data)

    def test_update_task(self):
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'completed',
            'priority': 'low',
            'user': self.user.id
        }
        # Update task
        response = self.client.put(reverse('tasks-detail', args=[self.task.id]), data, format='json')
        
        # Debugging output
        print(response.status_code)
        print(response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        
        # Check if cache is cleared
        cached_data = cache.get('tasks:')
        self.assertIsNone(cached_data)

    def test_delete_task(self):
        response = self.client.delete(reverse('tasks-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

        # Check if cache is cleared
        cached_data = cache.get('tasks:')
        self.assertIsNone(cached_data)

    def test_task_filter_by_status(self):
        response = self.client.get(reverse('tasks-list') + '?status=new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Verify caching works
        cached_data = cache.get(f"tasks:status=new")
        self.assertIsNotNone(cached_data)

    def test_task_filter_by_priority(self):
        response = self.client.get(reverse('tasks-list') + '?priority=medium')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Check cache population
        cached_data = cache.get(f"tasks:priority=medium")
        self.assertIsNotNone(cached_data)

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
        self.assertTrue(True)  # Ensure no error during WebSocket send
