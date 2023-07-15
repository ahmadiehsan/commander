import os
import subprocess

from commander.action import BaseAction
from commander.utils import asset


class Action(BaseAction):
    help = 'scaffold an empty project'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('project_name', help='project name', nargs='?', default='commander_empty_project')

    def run(self):
        commands = f"cp -r {asset('empty_project')}/. {os.path.join(os.environ['PWD'], self.arguments.project_name)}"
        subprocess.run(commands, shell=True, check=True)  # nosec
        print('Done!')
