import requests

from django.conf import settings
from core.models import Team, Space, Folder, List  # , Task

access_token = settings.CLICKUP_API_TOKEN
base_url = settings.CLICKUP_API_URL
req_headers = {"Authorization": access_token}


def get_teams() -> list:
    url = f"{base_url}team"
    teams = requests.get(url, headers=req_headers).json()
    return teams.get("teams")


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


def create_task(list_id: int, payload: dict) -> dict:
    # list_id 19430919
    url = f"{base_url}list/{list_id}/task"
    return requests.post(url, json=payload, headers=req_headers).json()


def create_webhook(team_id: int, payload: dict) -> dict:
    """Create a webhook through which we can receive events"""
    # team_id 2536606
    url = f"{base_url}team/{team_id}/webhook"
    return requests.post(url, json=payload, headers=req_headers).json()


def get_custom_fields(list_id: int) -> list:
    """Get Custom Fields for a list"""
    # list_id 19430894  or 19454627
    url = f"{base_url}list/{list_id}/field"
    fields = requests.get(url, headers=req_headers).json()
    return fields.get("fields")


# =======================================================================


def import_teams_data(team_id: int):
    print("Creating team representation...")
    # saving a new team with provided id
    saved_team, created = Team.objects.get_or_create(clickup_id=team_id)
    if not created:
        saved_team.is_active = False
        saved_team.save()

    team_name = None
    # getting rest of team info
    teams = get_teams()
    for team in teams:
        if str(team.get("id")) == str(team_id):
            print("current_team>>>>>>>>.\n", team)
            saved_team.name = team.get("name")
            team_name = team.get("name")
            saved_team.is_active = True
            saved_team.save()

    # Import Spaces for that team
    print("Getting Spaces...")
    spaces = get_spaces(team_id)
    print("Saving spaces representations to db...")
    saved_spaces = list()
    for space in spaces:
        current_space, created = Space.objects.get_or_create(clickup_id=space.get("id"))
        if created:
            current_space.is_active = False
        current_space.team = saved_team
        current_space.name = space.get("name")
        current_space.description = space.get("description")
        current_space.save()

        saved_spaces.append(current_space)

    # Import Folders for all imported spaces
    print("Getting folders for saved spaces...")
    saved_folders = list()
    for space in saved_spaces:
        folders = get_folders(space.clickup_id)
        for folder in folders:
            current_folder, created = Folder.objects.get_or_create(
                clickup_id=folder.get("id")
            )
            if created:
                current_folder.is_active = False
            current_folder.space = space
            current_folder.name = folder.get("name")
            current_folder.description = folder.get("description")
            current_folder.save()

            saved_folders.append(current_folder)

    # Import Lists for all imported folders
    print("Getting lists for saved folders...")
    saved_lists = list()
    for folder in saved_folders:
        lists = get_lists(folder.clickup_id)
        for list_ in lists:
            current_list, created = List.objects.get_or_create(
                clickup_id=list_.get("id")
            )
            if created:
                current_list.is_active = False
            current_list.folder = folder
            current_list.name = list_.get("name")
            current_list.description = list_.get("description")
            current_list.save()

            saved_lists.append(current_list)

    print("Done")

    return team_name

    # NOTE not even needed, reactivate when needed
    # print("Getting Tasks for saved lists...")
    # saved_tasks = list()
    # for list_ in saved_lists:
    #     tasks = get_tasks(list_.clickup_id)
    #     for task in tasks:
    #         current_task, created = Task.objects.get_or_create(clickup_id=task.get("id"))
    #         if created:
    #             current_task.is_active = False
    #         current_task._list = list_    # Import Spaces for that team
    #         current_task.status = task.get("status")
    #         current_task.name = task.get("name")
    #         current_task.description = task.get("description")
    #         current_task.save()

    #         saved_tasks.append(current_task)

    # print(f"{len(saved_tasks)} Tasks in the system")
