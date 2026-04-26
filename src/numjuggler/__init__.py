"""
NumJuggler

Package provides script mcnp.juggler. See its help for description.

"""
from __future__ import annotations

try:
    from .version import version
except ImportError:
    # When cloned directly from git, version.py is not here
    version = "git.development"
__version__ = version
