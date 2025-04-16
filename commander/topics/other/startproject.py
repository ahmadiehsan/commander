import subprocess
from pathlib import Path

from commander.i_action import IAction
from commander.logger import logger
from commander.utils.standard_directory import asset


class Action(IAction):
    help = "Scaffold an empty project"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("project_name", help="project name", nargs="?", default="commander_empty_project")

    def run(self):
        empty_project_path = asset("empty_project")
        destination_path = Path.cwd() / self.arguments.project_name  # pylint: disable=no-member
        command = ["cp", "-r", f"{empty_project_path}/.", destination_path]
        subprocess.run(command, check=True)  # noqa: S603
        logger.info("done")
