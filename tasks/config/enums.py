from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = "PENDING, Pending"
    IN_PROGRESS = "IN_PROGRESS,In_Progress"
    FINISHED = "FINISHED, Finished"
    CANCELLED = "CANCELLED, Cancelled"

class EventType(models.TextChoices):
    STATUS_CHANGE = "STATUS_CHANGE", "Status_Change"
    PRIORITY_UPDATED = "PRIORITY_UPDATED", "Priority_Updated"
    DEADLINE_CHANGED = "DEADLINE_CHANGED", "Deadline_Changed"

class PerformedBy(models.TextChoices):
    USER = "USER", "User"
    AI = "AI", "AI"