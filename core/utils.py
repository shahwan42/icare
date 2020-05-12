import requests

from django.conf import settings

access_token = settings.CLICKUP_API_TOKEN
base_url = settings.CLICKUP_API_URL
req_headers = {"Authorization": access_token}


def get_teams() -> list:
    url = f"{base_url}team"
    return requests.get(url, headers=req_headers).json()


def get_team(position: int) -> dict:
    return get_teams().get("teams")[position]


def get_spaces(team_id: int) -> list:
    # team_id 2536606
    url = f"{base_url}team/{team_id}/space?archived=false"
    spaces = requests.get(url, headers=req_headers).json()
    return spaces.get("spaces")


def get_space(space_id: int) -> dict:
    # space_id 2671955
    url = f"{base_url}space/{space_id}"
    space = requests.get(url, headers=req_headers).json()
    return space


def get_folders(space_id: int) -> list:
    # space_id 2671955
    url = f"{base_url}space/{space_id}/folder?archived=false"
    folders = requests.get(url, headers=req_headers).json()
    return folders.get("folders")


def get_folder(folder_id: int) -> dict:
    # folder_id 8969050
    url = f"{base_url}folder/{folder_id}"
    folder = requests.get(url, headers=req_headers).json()
    return folder


def get_lists(folder_id: int) -> list:
    # folder_id 8969050
    url = f"{base_url}folder/{folder_id}/list?archived=false"
    lists = requests.get(url, headers=req_headers).json()
    return lists.get("lists")


def get_folderless_lists(space_id: int) -> list:
    # space_id 2671955
    url = f"{base_url}space/{space_id}/list?archived=false"
    lists = requests.get(url, headers=req_headers).json()
    return lists.get("lists")


def get_list(list_id: int) -> dict:
    # list_id 19430919
    url = f"{base_url}list/{list_id}"
    return requests.get(url, headers=req_headers).json()


def get_tasks(list_id: int) -> list:
    # list_id 19430919
    url = f"{base_url}list/{list_id}/task?archived=false"
    tasks = requests.get(url, headers=req_headers).json()
    return tasks.get("tasks")


def get_task(task_id: str) -> dict:
    # task_id 56km54 56km4y
    url = f"{base_url}task/{task_id}"
    return requests.get(url, headers=req_headers).json()
