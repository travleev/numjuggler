from __future__ import annotations

from typing import Generator, TextIO, TYPE_CHECKING


import sys

from contextlib import contextmanager
from pathlib import Path

if TYPE_CHECKING:
    from os import PathLike


@contextmanager
def resolve_fname_or_stream(
    fname_or_stream: PathLike | str | TextIO | None, mode: str = "r"
) -> Generator[TextIO, None, None]:
    """Open stream by name or pass as if it's already opened.

    Parameters
    ----------
    fname_or_stream
        file name or handle or Path to open, if None use std stream
    mode
        opening mode (as in Path)

    Returns
    -------
    Context with opened stream
    """

    is_input = mode == "r"
    if fname_or_stream is None:
        if is_input:
            yield sys.stdin
        else:
            yield sys.stdout
    elif (is_input and hasattr(fname_or_stream, "read")) or (
        not is_input and hasattr(fname_or_stream, "write")
    ):
        yield fname_or_stream
    else:
        with Path(fname_or_stream).open(mode=mode) as fid:
            yield fid
