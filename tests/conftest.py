import pytest

from pathlib import Path


@pytest.fixture
def cd_tmpdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Temporarily switch to temp directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path
