import os
import subprocess
import sys


def action_name():
    return os.environ["RUNNING_ACTION_NAME"]


def topic_dir_path():
    return os.environ["RUNNING_TOPIC_DIR"]


def call_action(arguments: list):
    first_arg = sys.argv[0]  # somethings like ./run_action.py
    command = [first_arg, *arguments]
    subprocess.run(command, check=True)  # noqa: S603
