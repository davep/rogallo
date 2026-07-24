"""Provides support code for loading up icons."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Local imports.
from ....data import load_configuration


##############################################################################
@cache
def icon(name: str) -> str:
    """Get the icon for a given name.

    Args:
        name: The name of the icon to get.

    Returns:
        The icon for the given name.
    """
    if len(icon := getattr(load_configuration(), name, "?").strip()) < 1:
        return "?"
    return icon[0]


### icons.py ends here
