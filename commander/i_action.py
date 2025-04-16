class IAction:
    help = None
    topic_class = None

    _arguments = None

    def run(self):
        err_msg = f"'{type(self)}' is a subclasses of 'IAction' and must provide the 'run' method"
        raise NotImplementedError(err_msg)

    @classmethod
    def get_help(cls):
        if cls.help is None:
            err_msg = f"{cls} should either include a 'help' attribute, or override the 'get_help()' method"
            raise NotImplementedError(err_msg)

        return cls.help

    @staticmethod
    def add_arguments(parser):
        pass

    @property
    def arguments(self):
        if not self._arguments:
            err_msg = "'arguments' attribute is only accessible during the run-time"
            raise RuntimeError(err_msg)

        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value
