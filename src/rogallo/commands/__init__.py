"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .clipboard import CopyDocumentToClipboard, CopyLocationToClipboard
from .main import (
    AddLocationToBookmarks,
    ChangeCommandLineLocation,
    GoHome,
    JumpToCommandLine,
    JumpToDocument,
    Reload,
    SetHome,
    SetHomeToCurrentLocation,
    ToggleBookmarks,
    ToggleHistory,
    ToggleView,
)
from .navigation import Backward, Forward

##############################################################################
# Exports.
__all__ = [
    "AddLocationToBookmarks",
    "Backward",
    "ChangeCommandLineLocation",
    "CopyDocumentToClipboard",
    "CopyLocationToClipboard",
    "Forward",
    "GoHome",
    "JumpToCommandLine",
    "JumpToDocument",
    "Reload",
    "SetHome",
    "SetHomeToCurrentLocation",
    "ToggleBookmarks",
    "ToggleHistory",
    "ToggleView",
]


### __init__.py ends here
