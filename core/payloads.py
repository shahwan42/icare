from datetime import datetime
from django.conf import settings


def create_task_payload(
    name: str, content: str, due_date: datetime.date = None, *args, **kwargs
) -> dict:
    return {
        "name": name,
        "content": content,
        # "assignees": None,  # [183],
        # "tags": None,  # ["tag name 1"],
        # "status": "Open",
        # "priority": 3,  # 1 : Urgent, 2 : High, 3 : Normal, 4 : Low.
        "due_date": None,  # 1508369194377,
        # "due_date_time": False,
        # "time_estimate": None,  # 8640000,
        # "start_date": None,  # 1567780450202,
        # "start_date_time": False,
        # "notify_all": True,
        # "parent": None,
        # "links_to": None,
        # "custom_fields": [
        #     {"id": "0a52c486-5f05-403b-b4fd-c512ff05131c", "value": 23},
        #     {"id": "03efda77-c7a0-42d3-8afd-fd546353c2f5", "value": "Text field input"},
        # ],
    }


def create_webhook_payload(*args, **kwargs) -> dict:
    # default to taskUpdated only for now
    return {
        "endpoint": f"{settings.WEBSITE_URL}task_updated",
        "events": [
            # "taskCreated",
            "taskUpdated",
            # "taskDeleted",
            # "listCreated",
            # "listUpdated",
            # "listDeleted",
            # "folderCreated",
            # "folderUpdated",
            # "folderDeleted",
            # "spaceCreated",
            # "spaceUpdated",
            # "spaceDeleted",
            # "goalCreated",
            # "goalUpdated",
            # "goalDeleted",
            # "keyResultCreated",
            # "keyResultUpdated",
            # "keyResultDeleted",
        ],
    }
