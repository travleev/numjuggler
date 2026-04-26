from io import StringIO
from pathlib import Path
from textwrap import dedent
from typing import Iterable

import pytest

from numjuggler.parser import (
    Card,
    CID,
    _split_data,
    are_close_lists,
    get_cards_from_input,
    load_decode_buffer,
)

HERE = Path(__file__).parent
DATA = HERE / "data"
assert DATA.is_dir()


@pytest.fixture
def card_600177() -> Card:
    definition = [
        "600177 400 -1.00000e+00 $ WATER_LEFT\n",
        "          600003 -600421 601230 -600013 600011\n",
        "           Vol=1.335972e+01\n",
        "           imp:n=1.0   imp:p=1.0   U=5972  \n",
    ]
    card = Card(definition, ctype=3, pos=1, debug=StringIO())
    card.get_values()  # dvp: as in the old test, why not in constructor?
    return card


@pytest.mark.parametrize(
    "value, expected_name",
    [
        (-1, "comment"),
        (-2, "blankline"),
        (1, "message"),
        (2, "title"),
        (3, "cell"),
        (4, "surface"),
        (5, "data"),
    ],
)
def test_cid(value, expected_name):
    assert CID.get_name(value) == expected_name


def test_cid_bad_path():
    with pytest.raises(ValueError, match="No CID names with value 100"):
        CID.get_name(100)


def test_vol_param(card_600177: Card):
    assert "Vol=1.335972e+01" in card_600177.card()


def test_get_and_set_value(card_600177: Card):
    assert card_600177._get_value_by_type("u") == 5972
    assert card_600177._get_value_by_type("_not_existing") is None
    card_600177._set_value_by_type("u", 30)
    assert "U=30" in card_600177.card()
    assert card_600177._get_value_by_type("u") == 30


def test_print_debug(card_600177: Card):
    debug_text = card_600177.debug.getvalue()
    assert "Line" in debug_text


def test_card_get_inpt_with_bad_character():
    log = StringIO()
    card = Card(["1\t0 1"], ctype=3, pos=1, debug=log)
    card.get_input(check_bad_chars=True)
    assert "get_input: bad char" in log.getvalue()
    card = Card(["1\t0 1"], ctype=3, pos=1, debug=None)
    with pytest.raises(ValueError, match="Bad character"):
        card.get_input(check_bad_chars=True)


def test_suffix_and_prefix_properties():
    card = Card(["1 0 1\n"], ctype=3, pos=1)
    card.get_values()
    assert card.geom_prefix == ""
    assert card.geom_suffix == ""
    card.geom_prefix = "pfx"
    card.geom_suffix = "sfx"
    assert card.geom_prefix == "pfx"
    assert card.geom_suffix == "sfx"


def test_fc_card():
    log = StringIO()
    card = Card(["fc4 xxx\n"], ctype=5, pos=1, debug=log)
    card.get_values()
    card.get_input()
    log_result = log.getvalue()
    assert "xxx" in log_result


def test_card_get_refcells():
    card = Card(["1 0 1\n"], ctype=3, pos=1)
    card.get_values()
    # card.get_input()
    actual = card.get_refcells()
    assert actual == {1}
    card = Card(["1 0 1 #2\n"], ctype=3, pos=1)
    card.get_values()
    # card.get_input()
    actual = card.get_refcells()
    assert actual == {1, 2}


def test_card_get_geom():
    card = Card(["1 0 1\n"], ctype=3, pos=1)
    card.get_values()
    geom = card.get_geom()
    assert geom.strip() == "1"


def test_card_get_u():
    card = Card(["1 0 1\n"], ctype=3, pos=1)
    card.get_values()
    universe = card.get_u()
    assert universe is None
    card = Card(
        [
            "1 0 1\n",
            "        u=200\n",
        ],
        ctype=3,
        pos=1,
    )
    card.get_values()
    universe = card.get_u()
    assert universe == 200


def test_card_get_f():
    card = Card(["1 0 1\n"], ctype=3, pos=1)
    card.get_values()
    assert card.get_f() is None
    card = Card(
        [
            "1 0 1\n",
            "        fill=200\n",
        ],
        ctype=3,
        pos=1,
    )
    card.get_values()
    assert card.get_f() == 200
    assert card.get_f(300) == 300
    assert card.get_f() == 300
    assert card._get_value_by_type("fill") == 300


@pytest.mark.parametrize(
    "card,vals,expected,msg",
    [
        (
            Card(["1 0 1\n"], 3, 1),
            None,
            {"imp:n": 1},
            "expect `imp:n=1`, if importance is not specified",
        ),
        (
            Card(["1 0 1\n", "      imp:n=2\n"], 3, 1),
            {"n": 3.0},
            {"imp:n": 3.0},
            "expect `imp:n=3` with updated value",
        ),
        (
            Card(["1 0 1\n", "      imp:n=2\n"], 3, 1),
            None,
            {"imp:n": 2},
            "expect `imp:n=2`",
        ),
        (Card(["F4 1\n"], 5, 1), None, None, "expect None for non cell card"),
    ],
)
def test_card_get_imp(card, vals, expected, msg):
    card.get_values()
    actual = card.get_imp(vals)
    assert actual == expected, msg
    actual2 = card.get_imp()
    assert actual2 is actual, "Should return previously cached value"


@pytest.mark.parametrize(
    "card",
    [
        Card(["1 0 1\n"], 3, 1),
        Card(["1 0 1\n", "     fill=100\n"], 3, 1),
        Card(["1 0 1\n", "     fill 100\n"], 3, 1),
        Card(["1 0 1\n", "     fill 100 (1)\n"], 3, 1),
        Card(["1 0 1\n", "     fill 100 (10 10 10)\n"], 3, 1),
    ],
)
def test_card_remove_fill(card):
    card.get_values()
    card.remove_fill()
    card.get_f() is None


@pytest.mark.parametrize(
    "x,y,re,pci,expected",
    [
        ([1, 2], [1, 2], 0.0, None, True),
        ([1, 2], [1, 2, 3], 0.0, None, False),
        ([1, 2], [1, 3], 0.0, None, False),
        ([1, 2], [1.1, 2], 0.2, None, True),
        ([1, 2], [1.1, 2], 0.1, None, False),
        ([1, 2, 3, 100], [2, 4, 6, 100], 0.1, (0, 3), True),
        ([1, 2, 3], [2, 4, 6], 0.1, (0,), True),
        ([0.0, 0.0], [0.0, 1e-7], 1e-6, (0, 2), False),  # comparing to zero is to be absolute
        ([0.0, 1e-7], [0.0, 0.0], 1e-6, (0, 2), False),
        ([0.0, 0.0], [0.0, 0.0], 1e-6, (0, 2), True),
        ([0.0, 1e-7], [0.0, -1e-7], 1e-7, (0, 2), False),
        ([0.0, 1e-7], [0.0, -1e-7], 2, (0, 2), True),
        ([], [], 2, None, True),
    ],
)
def test_are_close_lists(x, y, re, pci, expected):
    actual = are_close_lists(x, y, re, pci)
    assert actual == expected


@pytest.mark.parametrize(
    "card,expected",
    [
        (Card(["1 0 1  \n"], 3, 1), "1 0 1  \n"),
        (Card(["1 0  1: 2\n"], 3, 1), "1 0 1:2  \n"),
        (Card(["1 0 ( 1 : 2 ) (3 : 4)\n"], 3, 1), "1 0 (1:2) (3:4)      \n"),
        # TODO @dvp2015: why we need these trailing spaces in expected?
    ],
)
def test_remove_spaces(card, expected):
    card.get_values()
    card.remove_spaces()
    assert card.card() == expected


def test_card_with_like():
    card = Card(["2 LIKE 1 BUT TRCL 20\n"], 3, 1)
    card.get_values()
    assert card.ctype == 3


def test_card_with_repetitions():
    card = Card(["F4 1 3i 5\n"], 5, 1)
    card.get_values()
    assert card.ctype == 5


@pytest.mark.parametrize(
    "card,wrap,expected",
    [
        (
            Card(
                [
                    "1 0 100000000000 100000000001 100000000002 100000000003 100000000004"
                    " 100000000005 100000000006 100000000007 100000000008 \n"
                ],
                3,
                1,
            ),
            False,
            (
                "1 0 100000000000 100000000001 100000000002 100000000003 100000000004"
                " 100000000005 100000000006 100000000007 100000000008 \n"
            ),
        ),
        (
            Card(
                [
                    "1 0 100000000000 100000000001 100000000002 100000000003 100000000004"
                    " 100000000005 100000000006 100000000007 100000000008 \n"
                ],
                3,
                1,
            ),
            True,
            dedent("""
               1 0 100000000000 100000000001 100000000002 100000000003 100000000004
                     100000000005 100000000006 100000000007 100000000008
            """)[1:-1]
            + " \n",
        ),
    ],
)
def test_card_wrap(card, wrap, expected):
    card.get_values()
    actual = card.card(wrap)
    assert actual == expected


@pytest.mark.parametrize(
    "encoding",
    [
        "utf8",
        pytest.param(
            "cp1251", marks=pytest.mark.xfail(reason="encoding auto detection fails on short texts")
        ),
        pytest.param(
            "ascii", marks=pytest.mark.xfail(reason="acsii encoding corrupts any non english text")
        ),
    ],
)
def test_load_decode_buffer(cd_tmpdir, encoding):
    text = "Something with Юникод valid for cp1251"
    path = Path("test.txt")
    path.write_text(text, encoding=encoding, errors="backslashreplace")
    actual = load_decode_buffer(path).getvalue()
    assert actual == text


@pytest.mark.parametrize(
    "inp, expected",
    [  # Note: split_data doesn't need \n at the end of lines
        (["tr1 0 0 2"], (["tr{:<1} 0 0 2"], [(1, "tr")], "TRn")),
        (["m1 00101 1"], (["m{:<1} 00101 1"], [(1, "mat")], "Mn")),
        (["f4 1"], (["f{:<1} {:<1}"], [(4, "tal"), (1, "cel")], "Fn")),
        (["fmesh1004"], (["fmesh{:<4}"], [(1004, "tal")], "fmesh")),
        (
            ["fmesh1004", "     orig 10 10 10"],
            (["fmesh{:<4}", "     orig 10 10 10"], [(1004, "tal")], "fmesh"),
        ),
    ],
)
def test_split_data(inp, expected):
    actual = _split_data(inp)
    assert actual == expected


def with_message_validator(cards: Iterable[Card]):
    first_card: Card = next(cards)
    assert first_card.ctype == CID.message


def continue_validator(cards: Iterable[Card]):
    first_card: Card = next(cards)
    assert first_card.ctype == CID.data


@pytest.mark.parametrize(
    "fname, validator",
    [("with_message.mcnp", with_message_validator), ("continue", continue_validator)],
)
def test_get_cards_from_input(fname, validator):
    actual = get_cards_from_input(DATA / fname)
    validator(actual)
