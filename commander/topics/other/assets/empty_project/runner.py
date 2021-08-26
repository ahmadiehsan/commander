#!/usr/bin/env python

import os

if __name__ == '__main__':
    os.environ['PROJECT_ABSOLUTE_PATH'] = os.path.dirname(os.path.abspath(__file__))

    try:
        from commander.runner import Runner
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Commander. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    runner = Runner()
    runner.run()
