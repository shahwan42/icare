from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import Spaces, Folders, Lists from ClickUp"

    def handle(self, *args, **kwargs):
        # Import Spaces
        # Import Folders
        # Import Lists
        self.stdout.write("Handling Imports...")
