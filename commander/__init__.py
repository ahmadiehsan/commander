import os
import sys

if os.environ.get('PROJECT_ABSOLUTE_PATH'):
    # running by ./runner.py
    project_absolute_path = os.environ['PROJECT_ABSOLUTE_PATH']

else:
    # running by `commander-admin` command
    project_absolute_path = os.path.dirname(os.path.abspath(__file__))
    os.environ['PROJECT_ABSOLUTE_PATH'] = project_absolute_path

sys.path.append(project_absolute_path)
