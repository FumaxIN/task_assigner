from rest_framework import permissions
from django.shortcuts import get_object_or_404

from task_assigner.models import Task


class IsAssignedToTask(permissions.BasePermission):
    """
    Custom permission to only allow users assigned to a task to view or edit it.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is assigned to the task
        task_id = view.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        return task.assigned_to == request.user