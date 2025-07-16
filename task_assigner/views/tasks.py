import logging
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import(
    OrderingFilter,
    CharFilter,
    FilterSet
)

from task_assigner.permissions import IsAssignedToTask

from utils.views.mixins import PartialUpdateModelMixin
from utils.views.base import BaseModelViewSetPlain

from task_assigner.models import Task
from task_assigner.serializers.tasks import TaskSerializer, AssignTaskSerializer
from task_assigner.models.enums import TaskStatus

logger = logging.getLogger('task_assigner')


class TaskFilter(FilterSet):
    """
    FilterSet for filtering tasks based on various fields.
    """
    status = CharFilter(field_name='status', lookup_expr='iexact')
    assigned_to = CharFilter(field_name='assigned_to__external_id', lookup_expr='iexact')
    type = CharFilter(field_name='type', lookup_expr='iexact')

    order_by = OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('deadline', 'deadline'),
        ),
        field_labels={
            'created_at': 'Created At',
            'deadline': 'Deadline'
        }
    )

class TaskViewSet(
    BaseModelViewSetPlain,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    PartialUpdateModelMixin
):
    """
    API endpoint that allows tasks to be created, retrieved, updated, and deleted.
    """
    queryset = Task.objects.all()
    lookup_field = 'external_id'
    filterset_class = TaskFilter
    permission_classes = (permissions.AllowAny,)
    # permission_action_classes = {
    #     'create': (permissions.IsAdminUser(),),
    #     'list': (permissions.AllowAny(),),
    #     'retrieve': (permissions.AllowAny(),),
    #     'partial_update': (permissions.IsAdminUser(),),
    #     'destroy': (permissions.IsAdminUser(),),
    #     'assign_task': (permissions.IsAuthenticated(),),
    #     'complete_task': (IsAssignedToTask(),),
    # }

    serializer_class = TaskSerializer
    serializer_action_classes = {
        'assign_task': AssignTaskSerializer,
    }

    def get_queryset(self):
        """
        Optionally restricts the returned tasks to a given user.
        """
        queryset = self.queryset
        external_id = self.request.query_params.get('external_id', None)
        if external_id:
            logger.info(f"Filtering tasks by external_id: {external_id}")
            queryset = queryset.filter(external_id=external_id)
        
        user = getattr(self.request, 'user', None)
        user_id = user.id if user and hasattr(user, 'id') else 'anonymous'
        logger.info(f"User {user_id} queried tasks, returned {queryset.count()} tasks")
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new task with logging.
        """
        user = getattr(request, 'user', None)
        user_id = user.id if user and hasattr(user, 'id') else 'anonymous'
        logger.info(f"User {user_id} attempting to create new task")
        
        try:
            response = super().create(request, *args, **kwargs)
            task_data = response.data
            task_title = task_data.get('title', 'Unknown')
            logger.info(f"Task created successfully: '{task_title}' by user {user_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to create task by user {user_id}: {str(e)}")
            raise

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task with logging.
        """
        user = getattr(request, 'user', None)
        user_id = user.id if user and hasattr(user, 'id') else 'anonymous'
        task = self.get_object()
        task_title = task.title if hasattr(task, 'title') else f"Task {task.external_id}"
        
        logger.info(f"User {user_id} attempting to delete task: '{task_title}'")
        
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Task deleted successfully: '{task_title}' by user {user_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to delete task '{task_title}' by user {user_id}: {str(e)}")
            raise


    @extend_schema(tags=['tasks'], description="Assign a task to a user.")
    @action(detail=False, methods=['post'])
    def assign_task(self, request, *args, **kwargs):
        """
        Assign a task to a user.
        """
        user = getattr(request, 'user', None)
        user_id = user.id if user and hasattr(user, 'id') else 'anonymous'
        
        logger.info(f"User {user_id} attempting to assign task")
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            
            task_title = task.title if hasattr(task, 'title') else f"Task {task.external_id}"
            assigned_to = task.assigned_to.email if hasattr(task, 'assigned_to') and task.assigned_to else 'Unknown'
            
            logger.info(f"Task assigned successfully: '{task_title}' assigned to {assigned_to} by user {user_id}")

            return Response(
                {
                    "message": "Task assigned successfully.",
                    "task": TaskSerializer(task, context=self.get_serializer_context()).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Failed to assign task by user {user_id}: {str(e)}")
            raise

    @extend_schema(tags=['tasks'], description="Complete a task.", request=None)
    @action(detail=True, methods=['post'])
    def complete_task(self, request, *args, **kwargs):
        """
        Mark a task as completed.
        """
        user = getattr(request, 'user', None)
        user_id = user.id if user and hasattr(user, 'id') else 'anonymous'
        
        task = self.get_object()
        task_title = task.title if hasattr(task, 'title') else f"Task {task.external_id}"
        
        logger.info(f"User {user_id} attempting to complete task: '{task_title}'")
        
        try:
            task.status = TaskStatus.COMPLETED
            task.completed_at = timezone.now()
            task.save()
            
            logger.info(f"Task completed successfully: '{task_title}' by user {user_id}")

            return Response(
                {
                    "message": "Task marked as completed.",
                    "task": TaskSerializer(task, context=self.get_serializer_context()).data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Failed to complete task '{task_title}' by user {user_id}: {str(e)}")
            raise