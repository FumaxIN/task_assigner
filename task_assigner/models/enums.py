from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.TextChoices):
    """
    Enum for task status.
    """
    UNASSIGNED = 'unassigned', _('Unassigned')
    PENDING = 'pending', _('Pending')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')
    FAILED = 'failed', _('Failed')


class TaskType(models.TextChoices):
    """
    Enum for task type.
    """
    URGENT = 'urgent', _('Urgent')
    NORMAL = 'normal', _('Normal')
    LOW = 'low', _('Low')
