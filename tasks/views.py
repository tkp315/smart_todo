from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Tasks, Categories, Task_History
from core.config.env_config import ENV_VARIABLES
from .config.enums import EventType
import json
import datetime

"""
Category-> 
1. create category 
3. fetch category details
4. fetch category order by usage_count
"""


"""
  Tasks->

1. create task -> done
2. get my tasks (status wise) ->done

3. update task -> endTime,startTime ->done
4. upload image
5. remove task 
6. get all tasks (satatus wise) -> done
7.filter
8. search
9. tasks by id ->done 

"""

"""
Task history->

1. get history of task 
2. get tasks by event

"""


@api_view(["POST"])
def create_category(request):
    payload = request.data["payload"]
    user = request.user
    is_dummy = request.is_dummy

    if not payload:
        Response({"error": "Payload is empty"}, status=status.HTTP_400_BAD_REQUEST)

    if not payload["name"]:
        Response({"error": "Name is missing"}, status=status.HTTP_400_BAD_REQUEST)

    category = Categories.objects.create(
        name=payload["name"],
        description=payload["description"],
        user_id=user.id if is_dummy == False else None,
    )

    Response(
        {"message": "Category  created successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def category_by_id(request):
    id = request.query_params.get("id")
    user = request.user

    if not id:
        Response({"error": "Category id required"}, status=status.HTTP_400_BAD_REQUEST)

    data = Categories.objects.get(id=id)
    print("category data", data)

    if not data:
        Response(
            {"message": "No category data found"}, status=status.HTTP_204_NO_CONTENT
        )

    # need to check once
    Response(
        {"message": "Successfully fetched data", "result": data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def categories(request):
    user = request.user
    is_dummy = request.is_dummy

    specific_user = True if is_dummy == False else False

    data = (
        Categories.objects.filter().order_by("-usage_count")
        if specific_user == False
        else Categories.objects.filter(user_id=user.id).order_by("-usage_count")
    )

    print("category data", data)

    if not data or len(data) == 0:
        Response(
            {"message": "No category data found"}, status=status.HTTP_204_NO_CONTENT
        )

    # need to check once
    Response(
        {"message": "Successfully fetched data", "result": data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def create_task(request):
    payload = request.data["payload"]
    user = request.user
    is_dummy = request.is_dummy

    specific_user = True if is_dummy == False else False

    required_fields = [
        payload["title"],
        payload["start_time"],
        payload["end_time"],
        payload["category_id"],
    ]

    for field in required_fields:
        if not field:
            Response(
                {"error": f"{field} is missing"}, status=status.HTTP_400_BAD_REQUEST
            )

    if payload["start_time"] > payload["end_time"]:
        Response(
            {"error": "Start time should be less than end time"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    task=Tasks.objects.create(
        title=payload["title"],
        description=payload["description"],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
        priority_reason=payload["priority_reason"],
        ai_generated_deadline=payload[" ai_generated_deadline"],
        category_id=payload["category_id"],
        user_id=user.id if specific_user == True else None,
    )

    Task_History.objects.create(
        event=EventType.CREATED,
        prev_event="NOT CREATED",
        current_event=EventType.CREATED,
        time=datetime.datetime.now(),
        notes = "TASK IS CREATED",
        task_id= task.id
    )

    Response({"message": "Task Created Successfully"}, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def update_task(request):
    payload = request.data["payload"]
    user = request.user
    is_dummy = request.is_dummy
    specific_user = True if is_dummy == False else False
    task = {}
    try:
        task = Tasks.objects.get(id=payload.get("id"))
    except Tasks.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    task.title = payload.get("title", task.title)
    task.description = payload.get("description", task.description)
    task.start_time = payload.get("start_time", task.start_time)
    task.end_time = payload.get("end_time", task.end_time)
    task.priority_reason = payload.get("priority_reason", task.priority_reason)
    task.ai_generated_deadline = payload.get(
        "ai_generated_deadline", task.ai_generated_deadline
    )
    
    task.is_finished= payload.get('is_finished')
    task.is_finished= payload.get('finished_at')
    task.category_id = payload.get("category_id", task.category_id)
    task.user_id = user.id if not is_dummy else task.user_id
    task.priority = payload.get("priority", task.priority)
    task.status = payload.get("status", task.status)
    task.is_timely_finished = payload.get("is_timely_finished", task.status)
    task.save()

   




    Response({"message": "Task Updated Successfully"}, status=status.HTTP_201_CREATED)


# Update fields only if provided, else keep existing
@api_view(["GET"])
def fetch_tasks(request):
    user = request.user
    is_dummy = request.is_dummy
    specific_user = True if is_dummy == False else False

    data = (
        Tasks.objects.filter()
        if specific_user == False
        else Tasks.objects.filter(user_id=user.id)
    )

    print("task data", data)

    if not data or len(data) == 0:
        Response({"message": "No Tasks  found"}, status=status.HTTP_204_NO_CONTENT)

    task_data = {
        "pending": [],
        "in_progress": [],
        "finished": [],
        "cancelled": [],
        "overdue": [],
    }

    for task in data:
        status = task["status"].lower()
        print("Status", status)
        if status == "pending":
            task_data["pending"].append(task)
        elif status == "in_progress":
            task_data["in_progress"].append(task)
        elif status == "cancelled":
            task_data["cancelled"].append(task)
        elif status == "finished":
            task_data["finished"].append(task)
        elif status == "overdue":
            task_data["overdue"].append(task)

    # need to check once
    Response(
        {"message": "Successfully fetched data", "result": task},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def task_by_id(request):
    id = request.query_params.get("id")
    user = request.user

    if not id:
        Response({"error": "Task id required"}, status=status.HTTP_400_BAD_REQUEST)

    data = Tasks.objects.get(id=id)
    print("task data", data)

    if not data:
        Response({"message": "No task data found"}, status=status.HTTP_404_NOT_FOUND)

    # need to check once
    Response(
        {"message": "Successfully fetched data", "result": data},
        status=status.HTTP_200_OK,
    )


def task_filter(request):
    payload = request.query_params.get("payload")

    if payload:
        payload = json.loads(payload)

    query = {
        "category_id": None,
        "recommendation_id": None,
        "priority": None,
        "status": None,
        "is_timely_finished": None,
    }

    for key in query.items():
        if key in payload and payload[key] is not None:
            query[key] = payload[key]
    filter = {k: v for k, v in query.items() if v is not None}
    tasks = Tasks.objects.filter(**filter).order_by("-created_at")

    if not tasks:
        Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)

    Response({"message": "Task fetched Successfully"}, status=status.HTTP_200_OK)


def task_search(request):
    title = request.query_params.get("title")

    tasks = Tasks.objects.filter(title_icontains=title).order_by("-created_at")

    if not tasks or not tasks.exists():
        Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)

    Response({"message": "Task fetched Successfully"}, status=status.HTTP_200_OK)


def remove_task(request):
    title = request.query_params.get("id")

    task = Tasks.objects.get(id=id)
    if not task or not task.exists():
        Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)

    task.delete()


    Response({"message": "Task deleted Successfully"}, status=status.HTTP_200_OK)

