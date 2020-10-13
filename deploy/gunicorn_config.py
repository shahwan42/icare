# copy to ./local_gunicorn_config.py

command = "/home/USERNAME/.virtualenvs/VENV_NAME/bin/gunicorn"
pythonpath = "/home/USERNAME/.virtualenvs/VENV_NAME/bin/python"
bind = "127.0.0.1:8003"
workers = 3
user = "USERNAME"
