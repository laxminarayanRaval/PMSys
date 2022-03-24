from rest_framework import serializers
from .models import Project, Permission, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name', 'desc', 'project_color_identity', 'created_by',
        )
