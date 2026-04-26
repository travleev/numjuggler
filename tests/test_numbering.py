from __future__ import annotations

import pytest

from numjuggler.numbering import _Range, LikeFunction, read_map_file


def test_range_class():
    r = _Range(1)
    assert 1 in r
    assert 2 not in r
    r = _Range(1, 3)
    assert 1 in r
    assert 2 in r
    assert 3 in r
    assert 4 not in r
    r = _Range(3, 1)
    assert 1 in r
    assert 2 in r
    assert 3 in r
    assert 0 not in r
    r = _Range("a", "z")
    assert "a" in r
    assert "z" in r
    assert "ab" in r
    assert "_" not in r


# @pytest.mark.xfail(reason="obsolete collections.Callable is used")
@pytest.mark.parametrize("pdict, n, expected", [({"c": [5, [(10, 20, 10)]]}, 1, 1+5)])
def test_like_function(pdict, n, expected):
    lf = LikeFunction(pdict)
    assert lf(n, "c") == expected
