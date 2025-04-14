from rest_framework import serializers
from task_assigner.models import User


class UserSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.SerializerMethodField(read_only=True)
    meta = serializers.SerializerMethodField(read_only=True)
    total_tasks_assigned = serializers.IntegerField(source='tasks.count', read_only=True)
    total_tasks_completed = serializers.SerializerMethodField(read_only=True)
    total_tasks_in_progress = serializers.SerializerMethodField(read_only=True)
    total_tasks_failed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'external_id',
            'email',
            'name',
            'completion_percentage',
            'total_tasks_assigned',
            'total_tasks_completed',
            'total_tasks_in_progress',
            'total_tasks_failed',
            'meta',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('external_id', 'created_at', 'updated_at', 'meta')

    def get_meta(self, obj):
        return {
            'is_admin': obj.is_admin,
            'is_staff': obj.is_staff,
            'is_superuser': obj.is_superuser
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_total_tasks_completed(self, obj):
        return obj.tasks.filter(status='completed').count()

    def get_total_tasks_in_progress(self, obj):
        return obj.tasks.filter(status='in_progress').count()

    def get_total_tasks_failed(self, obj):
        return obj.tasks.filter(status='failed').count()

    def get_completion_percentage(self, obj):
        total_tasks = obj.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = obj.tasks.filter(status='completed').count()
        return (completed_tasks / total_tasks) * 100

