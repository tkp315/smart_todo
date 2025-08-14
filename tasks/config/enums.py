from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = "PENDING, Pending"
    IN_PROGRESS = "IN_PROGRESS,In_Progress"
    FINISHED = "FINISHED, Finished"
    CANCELLED = "CANCELLED, Cancelled"
    OVERDUE="OVERDUE OVERDUE"

class EventType(models.TextChoices):
    STATUS_UPDATED = "STATUS_UPDATED", "Status_Updated"
    PRIORITY_UPDATED = "PRIORITY_UPDATED", "Priority_Updated"
    DEADLINE_UPDATED = "DEADLINE_UPDATED", "Deadline_Updated"
    CREATED = "CREATED", "Created"
    REMOVED = "REMOVED", "Removed"
    OTHER = "OTHER", "Other"
    

class PerformedBy(models.TextChoices):
    USER = "USER", "User"
    AI = "AI", "AI"