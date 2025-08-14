from core.config.env_config import ENV_VARIABLES

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

client = Anthropic(api_key=ENV_VARIABLES["ANTHROPIC_API_KEY"])


def analyze_daily_context(context_data):
    """
    context_data: list of daily context strings
    returns: summarized context and actionable insights as task and daily_context objects
    """

    system_prompt = """
    You are an AI assistant for task management and daily context analysis.
    Your job is to analyze the user's daily context and generate actionable tasks.
    You  summarize the context, detect urgent items, and suggest tasks.
    """

    # Include context_data in the prompt
    prompt = f"""
    I am providing you with a user's daily context in the form of a list of strings.
    Each string may be a WhatsApp message, email, note, or calendar event.
    This is step one for analysis

    Your task:
    1. Analyze the context to detect urgent and important items.
    2. Summarize insights from the context.
    3. Generate actionable tasks based on the context.
    4. For each task, provide a python dictionary object suitable for inserting into the Task model.
    5. For each context item related to a task, provide a python dictionary object suitable for inserting into the Daily_Context model.

    Context Data:
    {context_data}

    Rules:
    - Input is a list of strings called 'daily_context_input'.
    - Output should be two lists:
        a) task_objects: list of Task model python dictionary objects
        b) context_objects: list of Daily_Context model python dictionary objects
    - All IDs should be UUIDs.
    - Include relevant fields for both models (title, description, priority, status, start_time, end_time, user_id, category_id, recommendation_id, etc.)

    Example Input:
    daily_context_input = [
        # WhatsApp messages
        "WhatsApp: Hey, don't forget the team meeting tomorrow at 10 AM. Please prepare the sales report.",
        "WhatsApp: Can you review the new project proposal today? The client wants feedback by 5 PM.",

        # Notes
        "Note: Buy groceries after work – milk, eggs, bread, and fruits.",
        "Note: Call the electrician to fix the kitchen lights this weekend.",
        "Note: Plan the weekend family picnic and send invites to everyone by Friday.",

        # Emails
        "Email from boss: Please submit the Q2 performance report by Friday EOD. Make sure it includes all department metrics.",
        "Email from HR: Reminder: Complete your mandatory online training before the end of this month.",
        "Email from client: Can we reschedule our call from Thursday to Wednesday 3 PM? Let me know your availability.",

        # Calendar events
        "Calendar: Doctor's appointment on Wednesday at 4 PM.",
        "Calendar: Project brainstorming session on Thursday at 2 PM in Conference Room B.",
        "Calendar: Yoga class every Monday, Wednesday, and Friday at 6 AM."
    ]

    Example Output:
    task_objects = [
        {
            "id": "a3f1b2c4-5d6e-7f89-0123-456789abcdef",
            "title": "Finish Django AI Integration",
            "description": "Integrate AI module to automatically generate tasks based on daily context.",
            "image": "task_images/dummy_task_image.jpg",
            "start_time": "2025-08-13T16:00:00",
            "end_time": "2025-08-16T16:00:00",
            "priority": 0,
            "priority_reason": "Urgent client requirement",
            "status": "PENDING",
            "created_by": "AI",
            "is_finished": False,
            "finished_at": None,
            "is_timely_finished": True,
            "ai_generated_deadline": "3 days, 0:00:00",
            "created_at": "2025-08-13T16:00:00",
            "updated_at": "2025-08-13T16:00:00",
            "user_id": "b1c2d3e4-5f67-8901-2345-6789abcdef01",
        }
    ]

    context_objects = [
        {
            "id": "f1a2b3c4-5d6e-7f89-0123-456789abcdef",
            "source_type": "Email",
            "content": "Please submit the report by Friday.",
            "image": "context_image/dummy_context_image.jpg",
            "content_type": "text/plain",
            "time": "2025-08-13T16:00:00",
            "is_task_related": True,
            "created_at": "2025-08-13T16:00:00",
            "updated_at": "2025-08-13T16:00:00",
            "user_id": "b1c2d3e4-5f67-8901-2345-6789abcdef01",
            "linked_task_id": "a3f1b2c4-5d6e-7f89-0123-456789abcdef"
        }
    ]
    final result 
    result = {
        "task":task_object,
        "context":context_object
    }
    """
    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=HUMAN_PROMPT + prompt,
        temperature=0.5,
        system_prompt=system_prompt,
    )

    return response


def task_prioritization(task_data, category_data):
    """
    Takes a list of task dictionaries and category dictionaries.
    Uses AI to:
      - Prioritize tasks (1–10 scale)
      - Suggest realistic deadlines
      - Match to existing categories or create new ones
    Returns: Python dictionary with 'task_objects' and 'category_objects'.
    """

    system_prompt = """
    You are an AI assistant for task management.
    Your job is to analyze tasks, assign priorities, suggest deadlines, 
    and categorize tasks into existing or newly created categories.
    Follow the output format strictly.
    """

    prompt = f"""
    I am providing you:
    1. A list of tasks — each with 'id', 'title', and 'description'.
    2. A list of categories — each with 'id', 'name', and 'description'.

    Your Job:
    1. Analyze each task and assign:
       - priority (1 = lowest, 10 = highest urgency)
       - priority_reason (brief explanation)
       - ai_generated_deadline (duration string, e.g., "2 days, 4:00:00")
       - start_time and end_time in ISO 8601 UTC format
       - category_id (existing if matched, otherwise create new)
    2. If a task matches one of the provided categories, return the category_id.
    3. If no match, create a new category and return its details in 'category_objects'.

    OUTPUT RULES:
    - Return ONLY a valid Python dictionary with two keys: 
      'task_objects' and 'category_objects'.
    - task_objects: list of dicts with:
        id (string, same as input),
        start_time (ISO 8601 UTC, e.g., "2025-08-14T09:00:00Z"),
        end_time (ISO 8601 UTC),
        priority (integer 1–10),
        priority_reason (string),
        ai_generated_deadline (string),
        category_id (UUID string)
    - category_objects: list of dicts with:
        id (UUID string),
        name (string),
        description (string),
        usage_count (integer, default 0 if new),
        created_at (ISO 8601 UTC),
        updated_at (ISO 8601 UTC),
        user_id (string or null)
    - All timestamps must include 'Z' for UTC.
    - Do NOT include explanations or any text outside the dictionary.

    Example Input:

    tasks = [
        {{
            "id": "a3f1b2c4-5d6e-7f89-0123-456789abcdef",
            "title": "Finish Django AI Integration",
            "description": "Integrate AI module to automatically generate tasks from daily context."
        }}
    ]

    categories = [
        {{
            "id": "a2d4f5b6-7c89-4e12-9d34-5f6a7b8c9d01",
            "name": "Work",
            "description": "Tasks related to office work, projects, and deadlines.",
            "usage_count": 12,
            "created_at": "2025-08-10T09:15:23Z",
            "updated_at": "2025-08-13T14:42:11Z",
            "user_id": "b3e4f5a6-7890-4c12-8d45-6f7a8b9c0d23"
        }}
    ]

    Example Output:

    {{
        "task_objects": [
            {{
                "id": "a3f1b2c4-5d6e-7f89-0123-456789abcdef",
                "start_time": "2025-08-14T09:00:00Z",
                "end_time": "2025-08-16T09:00:00Z",
                "priority": 9,
                "priority_reason": "Urgent project deadline in 2 days.",
                "ai_generated_deadline": "2 days, 0:00:00",
                "category_id": "a2d4f5b6-7c89-4e12-9d34-5f6a7b8c9d01"
            }}
        ],
        "category_objects": []
    }}
    """

    response = client.completions.create(
        model="claude-3-opus-20240229",
        prompt=HUMAN_PROMPT + prompt,
        temperature=0.3,
        system_prompt=system_prompt,
    )

    return response


