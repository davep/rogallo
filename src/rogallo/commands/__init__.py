"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .clipboard import CopyDocumentToClipboard, CopyLocationToClipboard
from .main import (
    AddLocationToBookmarks,
    ChangeCommandLineLocation,
    ClearCache,
    GoHome,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    Reload,
    SetHome,
    SetHomeToCurrentLocation,
    StripeLinks,
    ToggleBookmarks,
    ToggleHistory,
    ToggleView,
)
from .navigation import Backward, Forward
from .search import SearchBookmarks, SearchHistory

##############################################################################
# Exports.
__all__ = [
    "AddLocationToBookmarks",
    "Backward",
    "ClearCache",
    "ChangeCommandLineLocation",
    "CopyDocumentToClipboard",
    "CopyLocationToClipboard",
    "Forward",
    "GoHome",
    "JumpToCommandLine",
    "JumpToDocument",
    "JumpToSidebar",
    "Reload",
    "SearchBookmarks",
    "SearchHistory",
    "SetHome",
    "SetHomeToCurrentLocation",
    "StripeLinks",
    "ToggleBookmarks",
    "ToggleHistory",
    "ToggleView",
]


### __init__.py ends here
