from django.db import models

# Create your models here.

"""
### **. recommendations**

- `id` (UUID, PK)
- `user_id` (FK → users.id)
- `action` (string) ← e.g., "generate_priority", "suggest_deadline"
- `input_data` (JSON) ← raw AI input
- `output_data` (JSON) ← AI response
- `time` (datetime)
- `created_at` (datetime)
- `updated_at` (datetime)
"""
import uuid


class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation_number = models.IntegerField(default=0)  # 0->2
    time_period = models.CharField(max_length=100, default="today")
    recommendation_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="recommendations"
    )

    category_id = models.OneToOneField(
        "tasks.Categories", on_delete=models.CASCADE, related_name="recommendation"
    )
    class Meta:
        db_table='recommendations'


class AI_Logs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=50)
    time = models.DateTimeField()
    input_data = models.JSONField(blank=True, null=True)
    output_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="ai_logs"
    )
    class Meta:
        db_table='ai_logs'
