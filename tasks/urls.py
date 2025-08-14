from django.urls import path
from . import views

urlpatterns = [
    path("category/add/", views.create_category, name="add_category"),
    path("category/id/", views.category_by_id, name="fetch_category_by_id"),
    path("categories/", views.categories, name="categories"),
    path("create/", views.create_task, name="create_task"),
    path("update/", views.update_task, name="update_task"),
    path("/", views.fetch_tasks, name="tasks"),
    path("id/", views.task_by_id, name="task_by_id"),
    path("filter/", views.task_filter, name="filter_task"),
    path("search/", views.task_search, name="search_task"),
    path("remove/", views.remove_task, name="remove_task"),
]
