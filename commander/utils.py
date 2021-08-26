import os
from pathlib import Path


def asset(*args, **kwargs):
    return _standard_directories_content_path_generator('assets', *args, **kwargs)


def resource(*args, **kwargs):
    return _standard_directories_content_path_generator('resources', *args, **kwargs)


def result(*args, **kwargs):
    return _standard_directories_content_path_generator('results', *args, **kwargs)


def _standard_directories_content_path_generator(standard_directory_name, *args, **kwargs):
    topic_dir = os.environ['RUNNING_TOPIC_DIR']
    topic_standard_directory_path = os.path.join(topic_dir, standard_directory_name)
    generated_path = os.path.join(topic_standard_directory_path, *args)

    if kwargs.get('mkdir'):
        Path(os.path.dirname(generated_path)).mkdir(parents=True, exist_ok=True)

    return generated_path
