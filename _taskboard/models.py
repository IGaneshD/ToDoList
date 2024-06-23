from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="task's Owner", default=0)
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="task's Title")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="task's Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True, default=None, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add uuid
    task_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return f'{self.title}'
    
    class Meta:

        ordering = ['due_date', 'title']
