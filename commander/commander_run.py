import argparse
import os
import sys
from pathlib import Path
from typing import ClassVar

from commander.i_topic import ITopic
from commander.logger import logger


class CommanderRun:
    topics: ClassVar = []
    topics_dir_path = os.environ["TOPICS_DIR_ABSOLUTE_PATH"]

    def __init__(
        self,
        after_detect_topic_hook=None,
        after_detect_action_hook=None,
        before_run_action_hook=None,
        after_run_action_hook=None,
    ):
        def null_function_topic_class(topic_class):  # pylint: disable=unused-argument
            pass

        def null_function_action_class(action_class):  # pylint: disable=unused-argument
            pass

        def null_function_action_obj(action_obj):  # pylint: disable=unused-argument
            pass

        self.after_detect_topic_hook = after_detect_topic_hook or null_function_topic_class
        self.after_detect_action_hook = after_detect_action_hook or null_function_action_class
        self.before_run_action_hook = before_run_action_hook or null_function_action_obj
        self.after_run_action_hook = after_run_action_hook or null_function_action_obj

    def run(self):
        self._fill_topics_and_actions()

        # create appropriate argparse
        nested_parser = self._generate_nested_parser()
        arguments = nested_parser.parse_args()

        # run action with user's entered args
        action_obj = self._get_running_action_obj(arguments)

        try:
            self.before_run_action_hook(action_obj)
        except Exception:  # pylint: disable=broad-except # noqa: BLE001
            logger.exception("Stopped at 'before_run_action_hook'")
            sys.exit()

        action_obj.run()

        try:
            self.after_run_action_hook(action_obj)
        except Exception:  # pylint: disable=broad-except # noqa: BLE001
            logger.exception("Stopped at 'after_run_action_hook'")
            sys.exit()

    def _fill_topics_and_actions(self):
        topics_dir_path = Path(self.topics_dir_path)
        topics_dir_names = [item.name for item in topics_dir_path.iterdir() if item.is_dir()]

        for topic_dir_name in topics_dir_names:
            if "__" in topic_dir_name:  # __ like __pycache__
                continue

            topic_dir_path = topics_dir_path / topic_dir_name
            actions_file_name = [item.name for item in topic_dir_path.iterdir() if item.is_file()]

            topic_class = self._get_topic_class(topic_dir_name)

            actions = []
            action_classes = []
            for action_file_name in actions_file_name:
                if ".py" not in action_file_name or "__" in action_file_name:  # __ like __init__.py
                    continue

                action_name = action_file_name.rsplit(".", 1)[0]  # remove .py format

                self._set_process_envs(topic_dir_path, action_name)

                action_class = self._get_action_class(topic_dir_name, action_name)
                action_class.topic_class = topic_class
                try:
                    self.after_detect_action_hook(action_class)
                except Exception:  # pylint: disable=broad-except # noqa: S112,BLE001
                    continue

                actions.append({"name": action_name, "class": action_class})
                action_classes.append(action_class)

            topic_class.action_classes = action_classes
            try:
                self.after_detect_topic_hook(topic_class)
            except Exception:  # pylint: disable=broad-except # noqa: S112,BLE001
                continue

            self.topics.append(
                {"name": topic_dir_name, "dir_path": topic_dir_path, "class": topic_class, "actions": actions}
            )

    @staticmethod
    def _get_action_class(topic_name, action_name):
        action_module = __import__(f"{topic_name}.{action_name}", fromlist=["object"])

        try:
            return action_module.Action
        except AttributeError:
            logger.exception(f"Please add Action class to {action_name}.py in {topic_name} topic")
            sys.exit()

    @staticmethod
    def _get_topic_class(topic_name):
        if topic_name == "other":  # `other` topic doesn't need to a "Topic" class
            return ITopic

        topic_module = __import__(f"{topic_name}", fromlist=["object"])
        try:
            return topic_module.Topic
        except AttributeError:
            logger.exception(f"Please add the 'Topic' class to '__init__.py' of '{topic_name}' topic")
            sys.exit()

    def _generate_nested_parser(self):
        main_parser = argparse.ArgumentParser()
        main_parser_subparsers = main_parser.add_subparsers(dest="topic")

        parsers = {}
        for topic in self.topics:
            topic_class = topic["class"]

            topic_parser = f"{topic['name']}_parser"
            topic_subparsers = f"{topic['name']}_subparsers"

            if topic["name"] == "other":
                # `other` topic's actions must run without `other` string in their command
                parsers[topic_subparsers] = main_parser_subparsers
            else:
                parsers[topic_parser] = main_parser_subparsers.add_parser(topic["name"], help=topic_class.get_help())
                parsers[topic_subparsers] = parsers[topic_parser].add_subparsers(dest="action")

            for action in topic["actions"]:
                action_parser = f"{action['name']}_parser"
                action_class = action["class"]
                parsers[action_parser] = parsers[topic_subparsers].add_parser(
                    action["name"], help=action_class.get_help()
                )
                action_class.add_arguments(parsers[action_parser])

        return main_parser

    def _get_running_action_obj(self, args):
        if not hasattr(args, "action"):
            # Actions of the `other` topic will run without the `other` string in their command,
            # so we will add it manually for the user
            args.action = args.topic
            args.topic = "other"

        selected_action = None
        for topic in self.topics:
            if topic["name"] == args.topic:
                for action in topic["actions"]:
                    if action["name"] == args.action:
                        self._set_process_envs(topic["dir_path"], action["name"])
                        selected_action = action["class"]

        if not selected_action:
            logger.error("Please enter a valid action")
            sys.exit()

        selected_action.arguments = args

        return selected_action()

    @staticmethod
    def _set_process_envs(topic_dir_path, action_name):
        os.environ["RUNNING_TOPIC_DIR"] = str(topic_dir_path)
        os.environ["RUNNING_ACTION_NAME"] = str(action_name)
