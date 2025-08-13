from django.db import models
import uuid

from .config.enums import TaskStatus, EventType, PerformedBy


# Create your models here.
class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=225)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='categories'


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="task_images/", blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    priority = models.IntegerField(default=0)  # 0->high, 1-> medium, 2-> low
    priority_reason = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30, choices=TaskStatus.choices, default=TaskStatus.PENDING
    )
    is_timely_finished = models.BooleanField(default=True)
    ai_generated_deadline = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="tasks"
    )

    category_id = models.OneToOneField(
        Categories, on_delete=models.CASCADE, related_name="tasks"
    )
    recommendation_id = models.ForeignKey(
        'ai_module.Recommendation',
        on_delete=models.CASCADE,
        related_name='tasks',
        blank=True,
        null=True
    )
    class Meta:
        db_table='tasks'

    def __str__(self):
        return self.title


class Task_History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event = models.CharField(choices=EventType.choices, max_length=50)
    prev_event = models.CharField(max_length=255)
    current_event = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(
        choices=PerformedBy.choices, max_length=50, default=PerformedBy.USER
    )
    notes = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    task_id = models.ForeignKey(
        Tasks, on_delete=models.CASCADE, related_name="task_history"
    )

    class Meta:
        db_table='task_history'
