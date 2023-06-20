#!/usr/bin/env python3
# coding=utf-8

import argparse
import logging
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
logger = logging.getLogger()


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] - %(message)s")
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    if verbosity > 0:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("-v", "--verbose", action="count", default=0)


def main(args: argparse.Namespace):
    _setup_logging(args.verbose)


def entry():
    add_arguments(parser)
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    entry()
