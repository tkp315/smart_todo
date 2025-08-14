from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from context.models import Daily_Context
from tasks.models import Tasks,Categories
from core.config.env_config import ENV_VARIABLES
from .anthropic_ai import analyze_daily_context,task_prioritization
import json
import datetime
import time

# Create your views here.

"""
1. analyse user's daily context 
Aggregate daily text data from multiple sources

Summarize key events, deadlines, and urgent messages

Detect context urgency (important vs low-priority)

Highlight actionable insights (tasks implied in messages)

--- then create tasks ------
--- create daily task schedule -------

"""

"""
2. tasks prioritization

fetch all tasks then 

1. prioritize tasks 
2. deadline updation 
3. categorize task 

if new task added then accordingly sort 
"""



"""
smart categorization 

"""

@api_view(['POST'])
def create_task_context(request):
    user = request.user
    is_dummy = request.is_dummy
    today = time.timezone.now().date()
    context =  Daily_Context.objects.filter(time=today) if is_dummy==True else Daily_Context.objects.filter(user_id=user.id,time=today)
    content = [ctx.content for ctx in context]

    ai_context_analysis_response = analyze_daily_context(content)

    print("AI context analysis",ai_context_analysis_response)

    # now create tasks 

    tasks_list_data = ai_context_analysis_response['task']
    task_list = []

    for task in tasks_list_data:
        t =Tasks.objects.create(
             title=task["title"],
        description=task["description"],
        start_time=task["start_time"],
        end_time=task["end_time"],
        priority_reason=task["priority_reason"],
        ai_generated_deadline=task[" ai_generated_deadline"],
        category_id=task["category_id"],
        user_id=user.id if is_dummy == False else None,
        )

        task_list.append(t)

        return Response({"message":"Task created successfully","created_tasks": [t.id for t in task_list]},status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_task_priority(request):
     user = request.user
     is_dummy = request.is_dummy

     tasks = Tasks.objects.filter(user_id=user.id) if is_dummy==False else  Tasks.objects.filter(user_id=user.id) 

     categories = Categories.objects.filter(user_id=user.id) if is_dummy==False else  Categories.objects.filter(user_id=user.id) 

     ai_task_data = task_prioritization(tasks,categories)

     if ai_task_data['category']:
         
         for cat in ai_task_data['category']:
             Categories.objects.create(
                 name=cat["name"],
        description=cat["description"],
        user_id=user.id if is_dummy == False else None,
             )
    
     for t in ai_task_data['task']:
         task = Tasks.objects.get(id=t.id);
         if task.ai_generated_deadline :
             continue
         task.start_time = task.get("start_time", task.start_time)
         task.end_time = task.get("end_time", task.end_time)
         task.priority_reason = task.get("priority_reason", task.priority_reason)
         task.priority = task.get("priority", task.priority)
         task.ai_generated_deadline =  task.get("ai_generated_deadline", task.ai_generated_deadline)
         task.save()

         return Response({"message":"Task updated successfully" },status=status.HTTP_200_OK)


   
    



