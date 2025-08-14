from django.urls import path
from . import views

urlpatterns = [
    path("context-analysis/", views.create_task_context, name="context_analysis"),
    path("update-task/", views.update_task_priority, name="update-task"),
]
