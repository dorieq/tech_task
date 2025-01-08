from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets, status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from order.utils.cache import add_cache_key, invalidate_task_cache

from .models import Task
from .serializer import TaskSerializer
from .pagination import TaskPagination

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'created_at']
    pagination_class = TaskPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cache_key = f"tasks:{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)
        
        # Cache the response if not found
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)  # Cache for 5 min
        
        # Track this cache key for later invalidation
        add_cache_key(cache_key)

        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_task_cache()  # Clear cache on task creation

    def perform_update(self, serializer):
        task = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'tasks',
            {
                'type': 'task_update',
                'message': f'Task \"{task.title}\" status updated to {task.status}'
            }
        )
        invalidate_task_cache()  # Clear cache on task update

    def perform_destroy(self, instance):
        instance.delete()
        invalidate_task_cache()  # Clear cache on task deletion
