from __future__ import annotations

from pathlib import Path
import sys

from numjuggler.utils import resolve_fname_or_stream


def test_resolve_fname_or_stream(cd_tmpdir):
    fname = "some.txt"
    path = Path(fname)
    text = "some text"
    assert not path.exists()
    with resolve_fname_or_stream(fname, mode="w") as fid:
        fid.write(text)
    assert path.exists(), "Should open a file, if file name is given as string"
    actual = path.read_text()
    assert actual == text, f"Expected content: {text}, not {actual}"
    with path.open() as fid:
        with resolve_fname_or_stream(fid, mode="w") as fid_passed:
            assert fid is fid_passed, "Should pass file object as is"
    with resolve_fname_or_stream(path) as fid:
        assert fid.read() == text, "Should open a file, if file is given as Path"
    with resolve_fname_or_stream(path, mode="w") as fid:
        fid.write(text)
    assert path.exists(), "Should create a file, if file name is given as Path"


def test_stdout(capsys):
    text = "for std"
    with resolve_fname_or_stream(None, mode="w") as fid:
        assert fid is sys.stdout
        fid.write(text)
    out, _ = capsys.readouterr()
    assert out == text


def test_stdin(capsys):
    with resolve_fname_or_stream(None) as fid:
        assert fid is sys.stdin
