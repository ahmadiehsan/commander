import os
import subprocess

from commander.action import BaseAction
from commander.utils import asset


class Action(BaseAction):
    help = 'scaffold an empty project'

    def add_arguments(self, parser):
        parser.add_argument(
            'project_name',
            help='project name',
            nargs='?',
            default='commander_empty_project'
        )

    def run(self, arguments):
        commands = """
        cp -r {empty_project_dir_path}/. {to}
        """.format(
            empty_project_dir_path=asset('empty_project'),
            to=os.path.join(os.environ['PWD'], arguments.project_name)
        )

        subprocess.run(commands, shell=True, check=True)
