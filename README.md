# ClickUp Tasks Board

An easy-to-use tasks board front-end for ClickUp

## Import Teams

- In the Admin panel, you create a new team with the team's clickup id,
you'll find the id in the link of your clickup.

for excample: this link, https://app.clickup.com/2536606/v/l/2dd4y-78?pr=2671955
here, the team's clickup_id = 2536606

- After adding select the team, than choose the "Import team's data" action
This will import all required team's Folders, Lists

## Import CustomFields

- Go to lists, and select all the lists, then choose the "Import custom fields" action

This will import the custom fields for the selected lists


## Activate Folders and Lists

- Go to Folders, click on folder's clickup_id and it will open the folder's details
- Is active? choose "yes"
- You'll find lists that are related to that folder, activate them according to your needs

## Create Webhook

- This command must run from the CLI and after importing the team's data
- `python manage.py create_webhook --team_id=ID_HERE`

