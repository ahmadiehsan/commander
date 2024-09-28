import os
import sys
from pathlib import Path

if os.environ.get('TOPICS_DIR_ABSOLUTE_PATH'):
    # running by ./run_action.py
    _TOPICS_DIR_ABSOLUTE_PATH = os.environ['TOPICS_DIR_ABSOLUTE_PATH']

else:
    # running by `commander-admin` command
    _TOPICS_DIR_ABSOLUTE_PATH = Path(__file__).resolve().parent / 'topics'
    os.environ['TOPICS_DIR_ABSOLUTE_PATH'] = str(_TOPICS_DIR_ABSOLUTE_PATH)

sys.path.append(str(_TOPICS_DIR_ABSOLUTE_PATH))
