import os
import subprocess
import sys


def action_name():
    return os.environ['RUNNING_ACTION_NAME']


def topic_dir_path():
    return os.environ['RUNNING_TOPIC_DIR']


def call_action(arguments: list):
    command = sys.argv[0]  # somethings like ./run_action.py

    for argument in arguments:
        command += ' ' + argument

    subprocess.run(command, shell=True, check=True)  # nosec
