import os
import warnings
from typing import Callable
import argparse
from datetime import datetime

class Registry:
    def __init__(self, managed_thing: str):
        """
        Create a new registry.

        Args:
            managed_thing: A string describing what type of thing is managed by this registry. Will be used for
                warnings and errors, so it's a good idea to keep this string globally unique and easily understood.
        """
        self.managed_thing = managed_thing
        self._registry = {}

    def register(self, name: str) -> Callable:
        def inner_wrapper(wrapped_class) -> Callable:
            if name in self._registry:
                warnings.warn(
                    f"{self.managed_thing} with name '{name}' doubly registered, old class will be replaced."
                )
            self._registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    def get_by_name(self, name: str):
        """Get a managed thing by name."""
        if name in self._registry:
            return self._registry[name]
        else:
            raise ValueError(f"{self.managed_thing} with name '{name}' unknown.")

    def get_all_names(self):
        """Get the list of things' names registered to this registry."""
        return list(self._registry.keys())


def prepare_dirs(files):
    """
    make dirs for each file
    """
    for file in files:
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))


def get_argparse_groups(args, parser):
    groups = {}
    for group in parser._action_groups:
        group_dict = {a.dest: getattr(args, a.dest, None) for a in group._group_actions}
        groups[group.title] = argparse.Namespace(**group_dict)
    return groups

def parse_daterange(date:str):
    start_date_str, end_date_str = date.split('_')
    start_date = None
    end_date = None
    if start_date_str != "":
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    if end_date_str != "":
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    return start_date, end_date

def merge_fasta(downloaded_stack, path):
    if len(downloaded_stack) <= 1:
        return
    with open(path, "w") as outfile:
        for filename in downloaded_stack:
            with open(filename, "r") as infile:
                outfile.write(infile.read())
    for file in downloaded_stack:
        os.remove(file)