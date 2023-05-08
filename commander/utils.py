import os
from pathlib import Path


def action_name():
    return os.environ['RUNNING_ACTION_NAME']


def topic_dir_path():
    return os.environ['RUNNING_TOPIC_DIR']


def asset(*args, **kwargs):
    return _standard_directories_content_path_generator('assets', *args, **kwargs)


def temp(*args, **kwargs):
    kwargs.update({'mkdir': True})

    return _standard_directories_content_path_generator('temps', *args, **kwargs)


def result(*args, **kwargs):
    kwargs.update({'mkdir': True})

    return _standard_directories_content_path_generator('results', *args, **kwargs)


def _standard_directories_content_path_generator(standard_directory_name, *args, **kwargs):
    topic_standard_directory_path = os.path.join(topic_dir_path(), standard_directory_name, action_name())
    generated_path = os.path.join(topic_standard_directory_path, *args)

    if kwargs.get('mkdir'):
        Path(os.path.dirname(generated_path)).mkdir(parents=True, exist_ok=True)

    return generated_path
