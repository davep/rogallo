"""Provides code for managing the application's configuration data.

The data in this module is intended to be all the user-supplied values that
will live in XDG_CONFIG_HOME.
"""

##############################################################################
# Local imports.
from .aliases import load_aliases
from .bindings import load_bindings
from .general import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .themes import load_themes
from .toolbar import ToolbarConfiguration, load_toolbar

##############################################################################
# Exports.
__all__ = [
    "Configuration",
    "load_aliases",
    "load_bindings",
    "load_configuration",
    "load_themes",
    "load_toolbar",
    "save_configuration",
    "ToolbarConfiguration",
    "update_configuration",
]

### __init__.py ends here
