"""Provides code for managing the application's state data.

The data in this module is intended to be all the application-usage values
that will live in XDG_STATE_HOME.
"""

##############################################################################
# Local imports.
from .command_history import (
    CommandLineHistory,
    load_command_history,
    save_command_history,
)
from .location_history import (
    LocationHistory,
    LocationVisit,
    load_location_history,
    save_location_history,
)
from .navigation_history import (
    NavigationHistory,
    NavigationPosition,
    load_navigation_history,
    save_naviagation_history,
)

##############################################################################
# Exports.
__all__ = [
    "CommandLineHistory",
    "load_command_history",
    "load_location_history",
    "load_navigation_history",
    "LocationHistory",
    "LocationVisit",
    "NavigationHistory",
    "NavigationPosition",
    "save_command_history",
    "save_location_history",
    "save_naviagation_history",
]

### __init__.py ends here
