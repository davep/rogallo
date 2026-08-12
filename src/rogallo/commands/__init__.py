"""Provides application-wide command-oriented messages."""

##############################################################################
# Local imports.
from .clipboard import CopyDocumentToClipboard, CopyLocationToClipboard
from .main import (
    AboutThisPage,
    AddLocationToBookmarks,
    ClearCache,
    HandOffToOperatingSystem,
    PipeDocument,
    Reload,
    SetHome,
    SetHomeToCurrentLocation,
    ToggleView,
    ViewChangeLog,
)
from .navigation import Backward, Forward, GoHome, GoToParent, GoToRoot, OpenFile
from .search import SearchBookmarks, SearchHistory
from .ui import (
    ChangeCommandLineLocation,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    StripeLinks,
    ToggleANSIEscapeSequenceHandling,
    ToggleBookmarksManager,
    ToggleCosyLinkNumbers,
    ToggleEmojiRemoval,
    ToggleHistoryManager,
    ToggleLinkNumbers,
)

##############################################################################
# Exports.
__all__ = [
    "AboutThisPage",
    "AddLocationToBookmarks",
    "Backward",
    "ChangeCommandLineLocation",
    "ClearCache",
    "CopyDocumentToClipboard",
    "CopyLocationToClipboard",
    "Forward",
    "GoHome",
    "GoToParent",
    "GoToRoot",
    "HandOffToOperatingSystem",
    "JumpToCommandLine",
    "JumpToDocument",
    "JumpToSidebar",
    "OpenFile",
    "PipeDocument",
    "Reload",
    "SearchBookmarks",
    "SearchHistory",
    "SetHome",
    "SetHomeToCurrentLocation",
    "StripeLinks",
    "ToggleANSIEscapeSequenceHandling",
    "ToggleBookmarksManager",
    "ToggleCosyLinkNumbers",
    "ToggleEmojiRemoval",
    "ToggleHistoryManager",
    "ToggleLinkNumbers",
    "ToggleView",
    "ViewChangeLog",
]


### __init__.py ends here
