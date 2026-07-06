"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .bookmarks import Bookmark, Bookmarks, load_bookmarks, save_bookmarks
from .command_history import (
    CommandLineHistory,
    load_command_history,
    save_command_history,
)
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .location_history import (
    LocationHistory,
    LocationVisit,
    load_location_history,
    save_location_history,
)
from .navigation_history import (
    NavigationHistory,
    load_navigation_history,
    save_naviagation_history,
)
from .trust import trust_file

##############################################################################
# Exports.
__all__ = [
    "Bookmark",
    "Bookmarks",
    "CommandLineHistory",
    "Configuration",
    "load_bookmarks",
    "load_command_history",
    "load_configuration",
    "load_location_history",
    "load_navigation_history",
    "LocationHistory",
    "LocationVisit",
    "NavigationHistory",
    "save_bookmarks",
    "save_command_history",
    "save_configuration",
    "save_location_history",
    "save_naviagation_history",
    "trust_file",
    "update_configuration",
]

### __init__.py ends here
