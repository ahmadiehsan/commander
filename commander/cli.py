import logging

from commander.commander_run import CommanderRun

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def commander_admin():
    commander_run = CommanderRun()
    commander_run.run()
