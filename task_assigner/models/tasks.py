from uuid import uuid4

from django.db import models

from .enums import TaskStatus, TaskType
from .users import User

class Task(models.Model):
    """
    Task model representing a task in the system.
    """
    external_id = models.UUIDField(default=uuid4, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.UNASSIGNED,
    )
    type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.NORMAL,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name