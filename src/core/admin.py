from django.contrib import admin
from .models import Project, Task, Permission

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Permission)