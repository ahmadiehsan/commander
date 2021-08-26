import subprocess


class BaseAction:
    help = None

    def run(self, *args, **kwargs):
        raise NotImplementedError('subclasses of BaseAction must provide a run() method')

    def get_help(self):
        assert self.help is not None, (
            f"{self.__class__.__name__} should either include a `help` attribute, "
            "or override the `get_help()` method."
        )
        return self.help

    def add_arguments(self, parser):
        pass


def call_action(arguments):
    command = './runner.py'

    for argument in arguments:
        command += ' ' + argument

    subprocess.run(command, shell=True, check=True)
