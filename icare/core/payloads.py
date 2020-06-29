from datetime import datetime
from django.conf import settings


def create_task_payload(
    name: str, content: str, due_date: datetime.date = None, *args, **kwargs
) -> dict:
    return {
        "name": name,
        "content": content,
        "due_date": due_date,  # 1508369194377,
        # TODO uncomment for custom fields
        # "custom_fields": [
        #     {"id": "0a52c486-5f05-403b-b4fd-c512ff05131c", "value": 23},
        #     {"id": "03efda77-c7a0-42d3-8afd-fd546353c2f5", "value": "Text field input"},
        # ],
    }


def create_webhook_payload(*args, **kwargs) -> dict:
    # default to taskUpdated only for now
    return {
        "endpoint": f"{settings.WEBSITE_URL}task_updated",
        "events": ["taskUpdated"],
    }
