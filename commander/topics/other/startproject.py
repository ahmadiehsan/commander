import subprocess
from pathlib import Path

from commander.i_action import IAction
from commander.utils.standard_directory import asset


class Action(IAction):
    help = 'Scaffold an empty project'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('project_name', help='project name', nargs='?', default='commander_empty_project')

    def run(self):
        commands = f"cp -r {asset('empty_project')}/. {Path.cwd() / self.arguments.project_name}"
        subprocess.run(commands, shell=True, check=True)  # nosec
        print('Done!')
