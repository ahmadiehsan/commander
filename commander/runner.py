import argparse
import os
import sys

import argcomplete


class Runner:
    topics = []
    topics_dir_path = os.environ['TOPICS_DIR_ABSOLUTE_PATH']

    def __init__(self, before_run_hook=None, after_run_hook=None):
        self.before_run_hook = before_run_hook if before_run_hook else lambda action_obj: None
        self.after_run_hook = after_run_hook if after_run_hook else lambda action_obj: None

    def run(self):
        self._fill_topics()

        # create appropriate argparse
        nested_parser = self._generate_nested_parser()
        arguments = nested_parser.parse_args()

        # run action with user's entered args
        action_obj = self._get_running_action_obj(arguments)

        self.before_run_hook(action_obj=action_obj)
        action_obj.run()
        self.after_run_hook(action_obj=action_obj)

    def _fill_topics(self):
        _, topics_dir_names, _ = next(os.walk(self.topics_dir_path))
        for topic_dir_name in topics_dir_names:
            if '__' not in topic_dir_name:  # __ like __pycache__
                topic_dir_path, _, actions_file_name = next(os.walk(os.path.join(self.topics_dir_path, topic_dir_name)))

                actions = []
                for action_file_name in actions_file_name:
                    if '.py' in action_file_name and '__' not in action_file_name:  # __ like __init__.py
                        action_name = action_file_name.rsplit('.', 1)[0]  # remove .py format

                        self._set_process_envs(topic_dir_path, action_name)

                        actions.append(
                            {'name': action_name, 'class': self._get_action_class(topic_dir_name, action_name)}
                        )

                if topic_dir_name == 'other':
                    topic_config_class = None  # `other` topic no need to config file
                else:
                    topic_config_class = self._get_topic_config_class(topic_dir_name)

                self.topics.append(
                    {
                        'name': topic_dir_name,
                        'dir_path': topic_dir_path,
                        'config_class': topic_config_class,
                        'actions': actions,
                    }
                )

    @staticmethod
    def _get_action_class(topic_name, action_name):
        action_module = __import__(f'{topic_name}.{action_name}', fromlist=['object'])

        try:
            return action_module.Action
        except AttributeError:
            print(f'Please add Action class to {action_name}.py in {topic_name} topic')
            sys.exit()

    @staticmethod
    def _get_topic_config_class(topic_name):
        topic_module = __import__(f'{topic_name}', fromlist=['object'])
        try:
            return topic_module.TopicConfig
        except AttributeError:
            print(f'Please add TopicConfig class to __init__.py of {topic_name} topic')
            sys.exit()

    def _generate_nested_parser(self):
        main_parser = argparse.ArgumentParser()
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
                action_class = action['class']
                parsers[action_parser] = parsers[topic_subparsers].add_parser(
                    action['name'], help=action_class.get_help()
                )
                action_class.add_arguments(parsers[action_parser])

        argcomplete.autocomplete(main_parser)
        return main_parser

    def _get_running_action_obj(self, args):
        if not hasattr(args, 'action'):
            # Actions of the `other` topic will run without the `other` string in their command,
            # so we will add it manually for the user
            args.action = args.topic
            args.topic = 'other'

        selected_action = None
        for topic in self.topics:
            if topic['name'] == args.topic:
                for action in topic['actions']:
                    if action['name'] == args.action:
                        self._set_process_envs(topic['dir_path'], action['name'])
                        selected_action = action['class']

        if not selected_action:
            print('Please enter a valid action')
            sys.exit()

        selected_action.arguments = args

        return selected_action()

    @staticmethod
    def _set_process_envs(topic_dir_path, action_name):
        os.environ['RUNNING_TOPIC_DIR'] = topic_dir_path
        os.environ['RUNNING_ACTION_NAME'] = action_name


def commander_admin():
    runner = Runner()
    runner.run()
