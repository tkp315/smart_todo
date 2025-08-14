from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_context, name="create_context"),
    path("fetch/", views.daily_contexts, name="daily_context")
    

]
