class ITopic:
    help = None
    action_classes = []

    @classmethod
    def get_help(cls):
        if cls.help is None:
            raise Exception(f'{cls} should either include a "help" attribute, or override the "get_help()" method.')

        return cls.help
