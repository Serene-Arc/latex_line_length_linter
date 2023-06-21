import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pytest

import linelengthlinter.__main__ as main


@dataclass(init=True)
class TestLine:
    length_limit: int
    is_comment: bool
    environments: Sequence[str] = ()


@pytest.fixture()
def test_file() -> Path:
    out = Path("tests", "test_document.tex")
    return out


def extract_line_numbers_from_output(output: Sequence[str]) -> Sequence[int]:
    pattern = re.compile(r":(\d+):.*?$")
    out = []
    for line in output:
        if line:
            match = pattern.search(line)
            number = int(match.group(1))
            out.append(number)
    return out


document_lines = {
    6: TestLine(0, False),
    9: TestLine(200, False),
    10: TestLine(200, False),
    13: TestLine(150, False),
    14: TestLine(150, False),
    17: TestLine(120, False),
    18: TestLine(120, False),
    21: TestLine(80, False),
    22: TestLine(80, False),
    25: TestLine(0, True),
    28: TestLine(120, True),
    29: TestLine(120, True),
    32: TestLine(80, True),
    33: TestLine(80, True),
    37: TestLine(0, False, ("float",)),
    40: TestLine(0, True, ("float",)),
    43: TestLine(100, False, ("float",)),
    44: TestLine(100, False, ("float",)),
    47: TestLine(80, False, ("float",)),
    48: TestLine(80, False, ("float",)),
    51: TestLine(120, True, ("float",)),
    52: TestLine(120, True, ("float",)),
    55: TestLine(80, True, ("float",)),
    56: TestLine(80, True, ("float",)),
    62: TestLine(0, False, ("float", "equation")),
    65: TestLine(0, True, ("float", "equation")),
    68: TestLine(100, False, ("float", "equation")),
    69: TestLine(100, False, ("float", "equation")),
    72: TestLine(80, False, ("float", "equation")),
    73: TestLine(80, False, ("float", "equation")),
    76: TestLine(120, True, ("float", "equation")),
    77: TestLine(120, True, ("float", "equation")),
    80: TestLine(80, True, ("float", "equation")),
    81: TestLine(80, True, ("float", "equation")),
    87: TestLine(0, False, ("equation",)),
    90: TestLine(0, True, ("equation",)),
    93: TestLine(100, False, ("equation",)),
    94: TestLine(100, False, ("equation",)),
    97: TestLine(80, False, ("equation",)),
    98: TestLine(80, False, ("equation",)),
    101: TestLine(120, True, ("equation",)),
    102: TestLine(120, True, ("equation",)),
    105: TestLine(80, True, ("equation",)),
    106: TestLine(80, True, ("equation",)),
}


@pytest.mark.parametrize(
    ("test_line_length", "test_include_comments", "test_exclude_environments"),
    (
        (200, False, ()),
        (200, True, ()),
        (80, False, ()),
        (80, True, ()),
        (80, True, ("float",)),
        (80, False, ("float",)),
        (80, True, ("equation",)),
        (80, False, ("equation",)),
    ),
)
def test_check_line_length(
    test_line_length: int,
    test_include_comments: bool,
    test_exclude_environments: Sequence[str],
    capsys: pytest.CaptureFixture,
    test_file: Path,
):
    main.check_line_length(test_file, test_line_length, test_include_comments, test_exclude_environments)
    out, err = capsys.readouterr()
    results = extract_line_numbers_from_output(out.split("\n"))

    expected = filter(lambda i: i[1].length_limit == 0 or i[1].length_limit > test_line_length, document_lines.items())
    if not test_include_comments:
        expected = filter(lambda i: i[1].is_comment is False, expected)
    expected = filter(lambda i: not any([e in i[1].environments for e in test_exclude_environments]), expected)
    assert results == sorted([i[0] for i in expected])
