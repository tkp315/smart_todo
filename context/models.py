from django.db import models
import uuid
from .config.enums import SourceType, ContentType

# Create your models here.


class Daily_Context(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    source_type = models.CharField(
        choices=SourceType.choices,
        max_length=60,
    )
    content = models.TextField()
    image = models.ImageField(upload_to="context_image/", blank=True, null=True)
    content_type = models.CharField(choices=ContentType.choices, max_length=100)
    time = models.DateTimeField()
    is_task_related = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="daily_context"
    )
    linked_task_id = models.OneToOneField(
        "tasks.Tasks",
        on_delete=models.CASCADE,
        related_name="daily_context",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "daily_context"
