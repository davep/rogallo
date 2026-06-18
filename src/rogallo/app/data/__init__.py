"""Provides functions and classes for managing the app's data."""

##############################################################################
# Local imports.
from .config import (
    Configuration,
    load_configuration,
    save_configuration,
    update_configuration,
)
from .trust import trust_file

##############################################################################
# Exports.
__all__ = [
    "Configuration",
    "load_configuration",
    "save_configuration",
    "trust_file",
    "update_configuration",
]

### __init__.py ends here
