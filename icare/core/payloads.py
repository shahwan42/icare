from datetime import datetime
from django.conf import settings


def create_task_payload(
    name: str, content: str, due_date: datetime.date = None, *args, **kwargs
) -> dict:
    return {
        "name": name,
        "content": content,
        "due_date": due_date,  # 1508369194377,
        # TODO attach file
    }


def create_webhook_payload(*args, **kwargs) -> dict:
    # default to taskUpdated only for now
    return {
        "endpoint": f"{settings.WEBSITE_URL}task_updated",
        "events": ["taskUpdated"],
    }
