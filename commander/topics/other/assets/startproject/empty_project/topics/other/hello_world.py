from commander.i_action import IAction


class Action(IAction):
    help = 'Hello world'

    def run(self):
        print('=========================')
        print('====== HELLO WORLD ======')
        print('=========================')
