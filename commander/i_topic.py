from typing import ClassVar


class ITopic:
    help = None
    action_classes: ClassVar = []

    @classmethod
    def get_help(cls):
        if cls.help is None:
            err_msg = f"{cls} should either include a 'help' attribute, or override the 'get_help()' method"
            raise NotImplementedError(err_msg)

        return cls.help
