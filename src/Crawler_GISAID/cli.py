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
        parser_.add_argument(
            "--tmp_dir",
            type=str,
            default="./tmp",
        )
    temp_args, _ = base_parser.parse_known_args()
    if temp_args.pipeline is None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if temp_args.tmp_dir is not None:
        tempfile.tempdir = os.path.abspath(temp_args.tmp_dir)
        os.makedirs(temp_args.tmp_dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(tempfile.tempdir, "basic.log"), level=logging.WARNING)
    print("logging at {}".format(os.path.join(tempfile.tempdir, "basic.log")))
    pipeline_cls = PipelineRegistry.get_by_name(temp_args.pipeline)
    pipeline_cls.setup_parser(parser)
    args = parser.parse_args()
    arg_groups = get_argparse_groups(args, parser)
    pipeline_cls(**vars(arg_groups["pipeline"]), **arg_groups)


def main():
    menu()