from __future__ import annotations

from pathlib import Path
import shutil

import pytest
import six
from numjuggler.main import main

HERE = Path(__file__).parent
test_data_path = HERE / "data"
assert test_data_path.exists(), "Cannot access test data files"


def load_line_heading_numbers(lines):
    res = []
    for line in lines:
        line = six.ensure_str(line, encoding="utf8")
        if line and str.isdigit(line[0]):
            if six.PY2:
                card_no = int(line.split()[0])
            else:
                card_no = int(line.split(maxsplit=2)[0])
            res.append(card_no)
    return res


@pytest.mark.parametrize(
    "inp,command,expected",
    [
        (
            "simple_cubes.mcnp",
            "-c 10",
            "11 12 13 14 15 16 17 1 2 3 4 5 6 7 20 21 22 23 24 25 30 31 32 33 34 35",
        ),
        (
            "simple_cubes.mcnp",
            "-c 20 -s 10",
            "21 22 23 24 25 26 27 11 12 13 14 15 16 17 30 31 32 33 34 35 40 41 42 43 44 45",
        ),
        pytest.param(
            "simple_cubes_with_multiline_tr.mcnp",
            "-c 20 -s 10",
            "21 22 23 24 25 26 27 11 12 13 14 15 16 17 30 31 32 33 34 35 40 41 42 43 44 45",
            marks=pytest.mark.xfail(reason="Failed on multiline TR specification"),
        ),
    ],
)
def test_rename(cd_tmpdir, capsys, inp, command, expected):
    source = test_data_path / inp
    wrk_file = shutil.copy(source, cd_tmpdir)
    command = command.split()
    command.append(str(wrk_file))
    main(command)
    out, _ = capsys.readouterr()
    actual_numbers = load_line_heading_numbers(out.split("\n"))
    expected_numbers = list(f for f in map(int, expected.split()))
    assert expected_numbers == actual_numbers, "Output of numjuggler is wrong"
