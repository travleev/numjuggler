from __future__ import annotations

import difflib
from io import StringIO
import sys

from pathlib import Path
import shutil
from typing import Iterable, Sequence

import pytest

from numjuggler.main import main

HERE = Path(__file__).parent.absolute()
data = HERE / "data/travis_tests"
assert data.exists(), "Cannot access test data 'travis' files"


@pytest.mark.parametrize(
    "mode,options,inp",
    [
        (
            "renum",
            "-c 10 -s 5 -m 100",
            "i1",
        ),
        (
            "renum",
            "-c i -s i -m i",
            "i2",
        ),
        (
            "renum",
            "-u -5942",
            "i3",
        ),
        pytest.param(
            "remh",
            "",
            "nested_complement",
            marks=pytest.mark.xfail(
                sys.platform == "win32", reason="Need more efforts on parser testing"
            ),
        ),
    ],
)
def test_mode_options_inp(cd_tmpdir, capsys, mode, options, inp):
    subdir = data / mode
    source = subdir / (inp + ".i")
    wrk_file = shutil.copy(source, cd_tmpdir)
    command = ["--mode", mode, *options.split(), wrk_file]
    main(command)
    out, _ = capsys.readouterr()
    ref_path = subdir / (inp + ".ref")
    _assert_str_path_equal(out, ref_path)


cdense_data = Path(data / "cdens")


@pytest.mark.parametrize("inp", ["inp"])
@pytest.mark.parametrize("map_", [f"map{x}" for x in range(1, 7)])
def test_cdens(cd_tmpdir, capsys, inp, map_):
    source = cdense_data / (inp + ".i")
    wrk_file = shutil.copy(source, cd_tmpdir)
    wrk_map = shutil.copy(cdense_data / map_, cd_tmpdir)
    command = ["--mode", "cdens", "--map", wrk_map, wrk_file]
    main(command)
    out, _ = capsys.readouterr()
    ref_path = cdense_data / f"{inp}.{map_}.ref"
    _assert_str_path_equal(out, ref_path)


merge_data = Path(data / "merge")


# TODO @dvp2015: numjuggler parser on Windows leaves <CR> before the closing quote `inp\r"`


@pytest.mark.parametrize(
    "inp,merged",
    [
        (
            "inp",
            "merged",
        )
    ],
)
def test_merge(cd_tmpdir, capsys, inp, merged):
    inp2_path = merge_data / (inp + "2.inp")
    inp1_path = merge_data / (inp + "1.inp")
    wrk_inp2 = shutil.copy(inp2_path, cd_tmpdir)
    wrk_inp1 = shutil.copy(inp1_path, cd_tmpdir)
    command = ["--mode", "merge", "-m", wrk_inp2, wrk_inp1]
    main(command)
    out, _ = capsys.readouterr()
    ref_path = merge_data / f"{merged}.{inp}.ref"
    _assert_str_path_equal(out, ref_path)


def assert_lines_equal(msg_prefix: str, lines_a: list[str], lines_b: list[str]) -> None:
    diff = list(difflib.Differ().compare(lines_a, lines_b))
    assert len(diff) == len(lines_a) == len(lines_b), msg_prefix + ":\n" + "".join(diff)


@pytest.mark.parametrize(
    "a, b",
    [
        (
            ["abc\n", "def\n"],
            ["abc\n", "def\n"],
        ),
        (
            ["abc\n", "def"],
            ["abc\n", "def"],
        ),
    ],
)
def test_assert_lines_equal(a, b):
    assert_lines_equal("xxx", a, b)


@pytest.mark.parametrize(
    "a, b",
    [
        (
            ["abc\n", "def\n"],
            ["cab\n", "def\n"],
        ),
        (
            ["abc\n", "def"],
            ["abc\n"],
        ),
    ],
)
def test_assert_lines_equal_when_not_equal(a, b):
    with pytest.raises(AssertionError, match="xxx"):
        assert_lines_equal("xxx", a, b)


def _assert_str_path_equal(out: str, ref_path: Path) -> None:
    with ref_path.open(encoding="utf8") as f:
        actual = StringIO(out).readlines()
        expected = f.readlines()
        if sys.platform == "win32":
            actual = [s.replace("\r", "") for s in actual]
            expected = [s.replace("\r", "") for s in expected]
        assert_lines_equal(ref_path.name, actual, expected)
