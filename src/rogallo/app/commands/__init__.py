"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .main import ChangeCommandLineLocation, JumpToCommandLine, JumpToDocument
from .navigation import Backward, Forward

##############################################################################
# Exports.
__all__ = [
    "Backward",
    "ChangeCommandLineLocation",
    "Forward",
    "JumpToCommandLine",
    "JumpToDocument",
]


### __init__.py ends here
