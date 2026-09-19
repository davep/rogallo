"""Provides code for loading keyboard bindings."""

##############################################################################
# Textual imports.
from textual.binding import Keymap

##############################################################################
# Local imports.
from ._io import load_configuration


##############################################################################
def load_bindings() -> Keymap:
    """Load the keyboard bindings.

    Returns:
        The loaded keyboard bindings.
    """
    return load_configuration("bindings", default={})


### bindings.py ends here
