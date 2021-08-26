import argparse
import importlib.util
import os
import sys

import argcomplete


class Runner:
    topics = []
    topics_dir = os.path.join(os.environ['PROJECT_ABSOLUTE_PATH'], 'topics')

    def run(self):
        self._fill_topics()

        # create appropriate argparse
        nested_parser = self._generate_nested_parser()
        arguments = nested_parser.parse_args()

        # run action with user's entered args
        action_obj = self._get_running_action_obj(arguments)
        action_obj.run(arguments)

    def _fill_topics(self):
        _, topics_dir_name, _ = next(os.walk(self.topics_dir))
        for topic_dir_name in topics_dir_name:
            topic_dir_path, _, actions_file_name = next(os.walk(os.path.join(self.topics_dir, topic_dir_name)))

            actions = []
            for action_file_name in actions_file_name:
                if 'py' in action_file_name and '__init__' not in action_file_name:
                    actions.append({
                        'name': action_file_name.rsplit('.', 1)[0],
                        'obj': self._get_action_obj(topic_dir_path, action_file_name)
                    })

            if topic_dir_name == 'other':
                topic_config_class = None  # `other` topic no need to config file
            else:
                topic_config_class = self._get_topic_config_class(topic_dir_path)

            self.topics.append({
                'name': topic_dir_name,
                'dir_path': topic_dir_path,
                'config_class': topic_config_class,
                'actions': actions
            })

    @staticmethod
    def _get_action_obj(topic_dir_path, action_file_name):
        action_file_path = os.path.join(topic_dir_path, action_file_name)
        spec = importlib.util.spec_from_file_location('', action_file_path)
        action_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(action_module)

        try:
            return action_module.Action()
        except AttributeError:
            print(f'Please add Action class in {action_file_path}')
            sys.exit()

    @staticmethod
    def _get_topic_config_class(topic_dir_path):
        try:
            spec = importlib.util.spec_from_file_location('', os.path.join(topic_dir_path, '__init__.py'))
            topic_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(topic_module)
            return topic_module.TopicConfig
        except FileNotFoundError:
            print(f'Please add __init__.py with TopicConfig class in {topic_dir_path}')
            sys.exit()

    def _generate_nested_parser(self):
        main_parser = argparse.ArgumentParser(description='Some useful but boring jobs is automated here :)')
        main_parser_subparsers = main_parser.add_subparsers(dest='topic')

        parsers = {}
        for topic in self.topics:
            topic_config_class = topic['config_class']

            topic_parser = f"{topic['name']}_parser"
            topic_subparsers = f"{topic['name']}_subparsers"

            if topic['name'] == 'other':
                # `other` topic's actions must run without `other` string in their command
                parsers[topic_subparsers] = main_parser_subparsers
            else:
                parsers[topic_parser] = main_parser_subparsers.add_parser(topic['name'], help=topic_config_class.help)
                parsers[topic_subparsers] = parsers[topic_parser].add_subparsers(dest='action')

            for action in topic['actions']:
                action_parser = f"{action['name']}_parser"
                action_obj = action['obj']
                parsers[action_parser] = parsers[topic_subparsers].add_parser(
                    action['name'],
                    help=action_obj.get_help()
                )
                action_obj.add_arguments(parsers[action_parser])

        argcomplete.autocomplete(main_parser)
        return main_parser

    def _get_running_action_obj(self, args):
        if not hasattr(args, 'action'):
            # `other` topic's actions run without `other` string in their command so we add it manually for user
            args.action = args.topic
            args.topic = 'other'

        for topic in self.topics:
            if topic['name'] == args.topic:
                self._set_process_envs(topic['dir_path'])

                for action in topic['actions']:
                    if action['name'] == args.action:
                        return action['obj']

    @staticmethod
    def _set_process_envs(topic_dir_path):
        os.environ['RUNNING_TOPIC_DIR'] = topic_dir_path


def commander_admin():
    runner = Runner()
    runner.run()
