from __future__ import annotations

import pytest

from numjuggler.utils import PartialFormatter


@pytest.mark.parametrize(
    "fmt, fillers, expected",
    [
        ("{a},{b}", {"a": 1, "b": 2}, "1,2"),
        ("{a},{b}", {"a": 1}, "1,{b}"),
        ("{a},{b}", {"a": 1, "b": 2, "c": 3}, "1,2"),
    ],
)
def test_partial_formatter(fmt, fillers, expected):
    assert PartialFormatter().format(fmt, **fillers) == expected


@pytest.mark.parametrize(
    "fmt, fillers, expected",
    [
        ("{a},{b}", {"a": 1, "b": 2}, "1,2"),
        ("{a},{b}", {"a": 1, "b": 2, "c": 3}, "1,2"),
    ],
)
def test_string_formatter(fmt, fillers, expected):
    assert fmt.format(fmt, **fillers) == expected


@pytest.mark.parametrize(
    "fmt, fillers, expected",
    [
        ("{a},{b}", {"a": 1}, "1,{b}"),
    ],
)
def test_string_formatter_bad_path(fmt, fillers, expected):
    with pytest.raises(KeyError, match="'b'"):
        fmt.format(fmt, **fillers) == expected


@pytest.mark.parametrize(
    "fmt, args, fillers, expected",
    [
        ("{},{a},{},{b}", ["x", "y"], {"a": 1, "b": 2}, "x,1,y,2"),
        ("{},{},{a},{b}", ["x", "y"], {"a": 1}, "x,y,1,{b}"),
        ("{a},{},{b},{}", ["x", "y"], {"a": 1, "b": 2, "c": 3}, "1,x,2,y"),
    ],
)
def test_partial_formatter_with_args(fmt, args, fillers, expected):
    assert PartialFormatter().format(fmt, *args, **fillers) == expected
