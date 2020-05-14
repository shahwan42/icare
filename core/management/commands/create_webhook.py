from django.core.management.base import BaseCommand
from core import utils as u, payloads as p
from core.models import CTeam, Webhook


class Command(BaseCommand):
    help = "Create webhook for a certain team"

    def add_arguments(self, parser):
        parser.add_argument("--team_id", nargs="+", type=int)

    def handle(self, *args, **options):
        # starting point
        team_id = options["team_id"][0]

        self.stdout.write("creating webhook to listen for task updates")
        # saving a new team with provided id
        qs = CTeam.objects.filter(c_id=team_id)
        if not qs.exists():
            exit("Run Import command first")

        saved_team = qs.first()
        breakpoint()

        resp = u.create_webhook(saved_team.c_id, p.create_webhook_payload())
        wh = Webhook.objects.create(
            c_team=saved_team, c_id=resp.get("id"), c_json_res=resp
        )

        self.stdout.write(f"webhook created {wh}")
