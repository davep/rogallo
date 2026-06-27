"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .clipboard import CopyDocumentToClipboard, CopyLocationToClipboard
from .main import (
    ChangeCommandLineLocation,
    JumpToCommandLine,
    JumpToDocument,
    Reload,
    ToggleHistory,
    ToggleView,
)
from .navigation import Backward, Forward

##############################################################################
# Exports.
__all__ = [
    "Backward",
    "ChangeCommandLineLocation",
    "CopyDocumentToClipboard",
    "CopyLocationToClipboard",
    "Forward",
    "JumpToCommandLine",
    "JumpToDocument",
    "Reload",
    "ToggleHistory",
    "ToggleView",
]


### __init__.py ends here
