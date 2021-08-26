from commander.action import BaseAction


class Action(BaseAction):
    help = 'hello world'

    def run(self, arguments):
        print('=========================')
        print('====== HELLO WORLD ======')
        print('=========================')
