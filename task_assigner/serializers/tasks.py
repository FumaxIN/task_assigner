from rest_framework import serializers
from django.shortcuts import get_object_or_404

from task_assigner.models import Task, User
from task_assigner.models.enums import TaskStatus
from .users import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """

    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'external_id',
            'name',
            'description',
            'assigned_to',
            'status',
            'type',
            'completed_at',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('external_id', 'created_at', 'updated_at', 'assigned_to')


class AssignTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning a task to a user.
    """

    user_id = serializers.UUIDField(write_only=True)
    task_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Task
        fields = ('user_id', 'task_id')

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        task_id = attrs.get('task_id')

        if not user_id:
            raise serializers.ValidationError("User ID is required.")

        if not task_id:
            raise serializers.ValidationError("Task ID is required.")

        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        task_id = validated_data.pop('task_id')

        try:
            task = get_object_or_404(Task, external_id=task_id)
            user = get_object_or_404(User, external_id=user_id)

            task.assigned_to = user
            task.status = TaskStatus.PENDING
            task.save()
            return task
        except Task.DoesNotExist:
            raise serializers.ValidationError("Task not found.")
