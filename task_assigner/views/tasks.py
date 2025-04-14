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
    #     'create': (permissions.IsAdminUser,),
    #     'list': (permissions.AllowAny,),
    #     'retrieve': (permissions.IsAuthenticated,),
    #     'partial_update': (permissions.IsAuthenticated,),
    #     'destroy': (permissions.IsAuthenticated,)
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
            queryset = queryset.filter(external_id=external_id)
        return queryset


    @extend_schema(tags=['tasks'], description="Assign a task to a user.")
    @action(detail=False, methods=['post'])
    def assign_task(self, request, *args, **kwargs):
        """
        Assign a task to a user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        return Response(
            {
                "message": "Task assigned successfully.",
                "task": TaskSerializer(task, context=self.get_serializer_context()).data
            },
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['tasks'], description="Complete a task.", request=None)
    @action(detail=True, methods=['post'])
    def complete_task(self, request, *args, **kwargs):
        """
        Mark a task as completed.
        """
        task = self.get_object()
        task.status = TaskStatus.COMPLETED
        task.completed_at = timezone.now()
        task.save()

        return Response(
            {
                "message": "Task marked as completed.",
                "task": TaskSerializer(task, context=self.get_serializer_context()).data
            },
            status=status.HTTP_200_OK
        )