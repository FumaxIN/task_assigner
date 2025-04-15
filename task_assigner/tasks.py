from celery import shared_task

from django.utils import timezone

from .models import Task
from .models.enums import TaskStatus


@shared_task
def expire_tasks():
    """
    Task to expire tasks that are past their deadline.
    """
    expired_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=[TaskStatus.UNASSIGNED, TaskStatus.PENDING, TaskStatus.IN_PROGRESS],
        completed_at=None,
    )

    for task in expired_tasks:
        task.status = TaskStatus.FAILED
        task.save()
    return f"Expired {expired_tasks.count()} tasks."

