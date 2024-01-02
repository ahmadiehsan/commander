from commander.i_action import IAction


class Action(IAction):
    help = 'hello world'

    def run(self):
        print('=========================')
        print('====== HELLO WORLD ======')
        print('=========================')
