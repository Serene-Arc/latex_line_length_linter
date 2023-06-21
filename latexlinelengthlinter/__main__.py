import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Sequence

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


def load_ignore_envs(ignore_envs_arg, ignore_envs_file):
    ignore_envs = []

    if ignore_envs_arg is not None:
        for arg in ignore_envs_arg:
            ignore_envs.extend(re.split(r"[, ]", arg))
    if ignore_envs_file is not None:
        for filename in ignore_envs_file:
            with open(filename, "r") as file:
                for line in file:
                    ignore_envs.append(line.strip())

    return ignore_envs


def check_line_length(
    filename: Path,
    max_length: int,
    check_comment_line_length: bool,
    environments_to_ignore: Sequence[str],
) -> bool:
    environment_stack = []

    file_incorrectly_formatted = False
    with open(filename, "r") as file:
        for i, line in enumerate(file, start=1):
            # check for the start of an environment
            env_start_pattern = re.compile(r"\s*\\begin\{(" + "|".join(environments_to_ignore) + ")}")
            env_start_match = env_start_pattern.match(line)
            if env_start_match:
                environment_stack.append(env_start_match.group(1))

            # check for the end of an environment
            env_end_pattern = re.compile(r"\s*\\end\{(" + "|".join(environments_to_ignore) + ")}")
            env_end_match = env_end_pattern.match(line)
            if env_end_match:
                if env_end_match.group(1) == environment_stack[-1]:
                    environment_stack.pop()
                else:
                    # this shouldn't ever happen
                    logger.warning(
                        f"Environment '{env_end_match.group(1)}' ended before previous "
                        f"environment '{environment_stack[-1]}'"
                    )

            if environment_stack:
                ignore_flag = True
            else:
                ignore_flag = False

            # ignore lines if inside an environment or (optionally) if it is a comment.
            is_comment = line.strip().startswith("%")
            if ignore_flag or (is_comment and not check_comment_line_length) or len(line.rstrip("\n")) <= max_length:
                continue
            else:
                print(f"{filename}:{i}: Line is longer than {max_length} characters")
                file_incorrectly_formatted = True

    return file_incorrectly_formatted


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    parser.add_argument("--max-length", type=int, default=80, help="Maximum line length")
    parser.add_argument("--ignore-comments", action="store_false", help="Ignore comments")
    parser.add_argument(
        "--ignore-envs",
        type=str,
        action="append",
        help="Additional environments to ignore (comma-separated)",
    )
    parser.add_argument(
        "--ignore-envs-file",
        type=str,
        action="append",
        help="File containing environments to ignore (one per line)",
    )
    parser.add_argument("--ignore-starred-envs", type=str, help="Whether to ignore all starred ignored envs")


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    ignore_envs = load_ignore_envs(args.ignore_envs, args.ignore_envs_file)

    if args.ignore_starred_envs:
        ignore_envs = [re.escape(e) + r"\*?" for e in ignore_envs]

    return_value = 0
    for filename in args.filenames:
        filename = Path(filename).expanduser().resolve()
        if not filename.exists():
            logger.error(f"Cannot find file at {filename}")
        else:
            if check_line_length(filename, args.max_length, args.ignore_comments, ignore_envs):
                return_value = 1
    sys.exit(return_value)


if __name__ == "__main__":
    main()
