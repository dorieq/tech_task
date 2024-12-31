from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets, status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)  # Cache for 5 min
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete('tasks_list')  # Clear cache after creating task

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('tasks_list')  # Clear cache after updating task

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('tasks_list')  # Clear cache after deleting task

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        task.status = request.data.get('status', task.status)
        task.save()
        cache.delete('tasks_list')  # Clear cache after status update
        return Response(
            {'status': 'Task updated'}, 
            status=status.HTTP_200_OK
        )
