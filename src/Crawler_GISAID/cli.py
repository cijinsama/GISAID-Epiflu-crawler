import argparse
import sys
import tempfile
import os
import logging
from .util import get_argparse_groups
from .pipeline import PipelineRegistry

def menu():
    base_parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.RawTextHelpFormatter
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    for parser_ in (base_parser, parser):
        parser_.add_argument(
            "pipeline",
            type=str,
            choices=PipelineRegistry.get_all_names(),
        )
    temp_args, _ = base_parser.parse_known_args()
    if temp_args.pipeline is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    pipeline_cls = PipelineRegistry.get_by_name(temp_args.pipeline)
    pipeline_cls.setup_parser(parser)
    args = parser.parse_args()
    arg_groups = get_argparse_groups(args, parser)
    pipeline_cls(**vars(arg_groups["pipeline"]), **arg_groups)


def main():
    menu()