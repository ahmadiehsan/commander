#!/usr/bin/env python

import os
from pathlib import Path

if __name__ == '__main__':
    os.environ['TOPICS_DIR_ABSOLUTE_PATH'] = str(Path(__file__).resolve().parent / 'topics')

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
