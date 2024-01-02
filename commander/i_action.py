class IAction:
    help = None
    topic_class = None

    _arguments = None

    def run(self):
        raise NotImplementedError(f'"{type(self)}" is a subclasses of "IAction" and must provide the "run" method')

    @classmethod
    def get_help(cls):
        if cls.help is None:
            raise Exception(f'{cls} should either include a "help" attribute, or override the "get_help()" method.')

        return cls.help

    @staticmethod
    def add_arguments(parser):
        pass

    @property
    def arguments(self):
        if not self._arguments:
            raise Exception('The "arguments" attribute is only accessible during the run-time')

        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value
