from django.core.management.base import BaseCommand
from core import utils as u
from core.models import Team, Space, Folder, List  # , Task


class Command(BaseCommand):
    help = "Import Spaces, Folders, Lists from ClickUp"

    def add_arguments(self, parser):
        parser.add_argument("--team_id", nargs="+", type=int)

    def handle(self, *args, **options):
        # starting point
        team_id = options["team_id"][0]

        self.stdout.write("Creating team representation...")
        # saving a new team with provided id
        saved_team, created = Team.objects.get_or_create(clickup_id=team_id)

        # getting rest of team info
        teams = u.get_teams()
        for team in teams:
            if str(team.get("id")) == str(team_id):
                saved_team.name = team.get("name")
                saved_team.is_active = True
                saved_team.save()

        # Import Spaces for that team
        self.stdout.write("Getting Spaces...")
        spaces = u.get_spaces(team_id)
        self.stdout.write("Saving spaces representations to db...")
        saved_spaces = list()
        for space in spaces:
            current_space, created = Space.objects.get_or_create(
                clickup_id=space.get("id")
            )
            if created:
                current_space.is_active = False
            current_space.team = saved_team
            current_space.name = space.get("name")
            current_space.description = space.get("description")
            current_space.save()

            saved_spaces.append(current_space)

        # Import Folders for all imported spaces
        self.stdout.write("Getting folders for saved spaces...")
        saved_folders = list()
        for space in saved_spaces:
            folders = u.get_folders(space.clickup_id)
            for folder in folders:
                current_folder, created = Folder.objects.get_or_create(
                    clickup_id=folder.get("id")
                )
                if created:
                    current_folder.is_active = False
                current_folder.c_space = space
                current_folder.name = folder.get("name")
                current_folder.description = folder.get("description")
                current_folder.save()

                saved_folders.append(current_folder)

        # Import Lists for all imported folders
        self.stdout.write("Getting lists for saved folders...")
        saved_lists = list()
        for folder in saved_folders:
            lists = u.get_lists(folder.clickup_id)
            for list_ in lists:
                current_list, created = List.objects.get_or_create(
                    clickup_id=list_.get("id")
                )
                if created:
                    current_list.is_active = False
                current_list.c_folder = folder
                current_list.name = list_.get("name")
                current_list.description = list_.get("description")
                current_list.save()

                saved_lists.append(current_list)

        self.stdout.write("Done")

        # NOTE not even needed, reactivate when needed
        # self.stdout.write("Getting Tasks for saved lists...")
        # saved_tasks = list()
        # for list_ in saved_lists:
        #     tasks = u.get_tasks(list_.clickup_id)
        #     for task in tasks:
        #         current_task, created = Task.objects.get_or_create(clickup_id=task.get("id"))
        #         if created:
        #             current_task.is_active = False
        #         current_task._list = list_
        #         current_task.status = task.get("status")
        #         current_task.name = task.get("name")
        #         current_task.description = task.get("description")
        #         current_task.save()

        #         saved_tasks.append(current_task)

        # self.stdout.write(f"{len(saved_tasks)} Tasks in the system")
