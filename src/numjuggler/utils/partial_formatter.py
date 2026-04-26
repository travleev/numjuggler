"""PartialFormatter module"""

from __future__ import annotations

import string


def _make_label(item: str) -> str:
    return "{" + item + "}" if item else ""


class _SafeDict(dict):
    def __getitem__(self, item: str) -> str:
        return super().__getitem__(item) or ""

    def __missing__(self, key):
        return _make_label(key)


class PartialFormatter(string.Formatter):
    """Formatter for incomplete fillers specification.

    For cases when not all of the fillers in a template
    are provided. Standard string.formatter throws KeyError
    in this case.

    Useful for formatting in several steps.
    """

    def format(self, format_string, /, *args, **kwargs):
        """Safely formats even if not fillers are provided in the kwargs."""
        return self.vformat(format_string, args, _SafeDict(kwargs))
