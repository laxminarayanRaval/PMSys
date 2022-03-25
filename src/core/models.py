from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    project_color_identity = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    task_name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    proj_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name


class Permission(models.Model):
    class Meta:
        unique_together = (('proj_id', 'user_id'),)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    proj_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    permit_name = models.CharField(max_length=100, choices=(('view', 'View'), ('edit', 'Edit'), ('delete', 'Delete')),
                                   default='view')
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.permit_name
