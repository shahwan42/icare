from django.core.management.base import BaseCommand
from ctb.core import utils as u


class Command(BaseCommand):
    help = "Import Spaces, Folders, Lists from ClickUp"

    def add_arguments(self, parser):
        parser.add_argument("--team_id", nargs="+", type=int)

    def handle(self, *args, **options):
        # starting point
        team_id = options["team_id"][0]

        u.import_teams_data(team_id)
