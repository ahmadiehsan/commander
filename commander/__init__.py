import os
import sys

if os.environ.get('TOPICS_DIR_ABSOLUTE_PATH'):
    # running by ./action_runner.py
    _TOPICS_DIR_ABSOLUTE_PATH = os.environ['TOPICS_DIR_ABSOLUTE_PATH']

else:
    # running by `commander-admin` command
    _TOPICS_DIR_ABSOLUTE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topics')
    os.environ['TOPICS_DIR_ABSOLUTE_PATH'] = _TOPICS_DIR_ABSOLUTE_PATH

sys.path.append(_TOPICS_DIR_ABSOLUTE_PATH)
