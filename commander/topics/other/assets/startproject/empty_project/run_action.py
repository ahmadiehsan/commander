#!/usr/bin/env python

import os

if __name__ == '__main__':
    os.environ['TOPICS_DIR_ABSOLUTE_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topics')

    try:
        from commander.commander_run import CommanderRun
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Commander. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    commander_run = CommanderRun()
    commander_run.run()
