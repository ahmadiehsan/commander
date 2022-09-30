import subprocess
import sys


class BaseAction:
    help = None

    def run(self, arguments):
        raise NotImplementedError(f'{self.__class__} is a subclasses of BaseAction and must provide a run() method')

    @classmethod
    def get_help(cls):
        assert cls.help is not None, (
            f'{cls} should either include a `help` attribute, ' 'or override the `get_help()` method.'
        )
        return cls.help

    @staticmethod
    def add_arguments(parser):
        pass


def call_action(arguments: list):
    command = sys.argv[0]  # somethings like ./action_runner.py

    for argument in arguments:
        command += ' ' + argument

    subprocess.run(command, shell=True, check=True)  # nosec
