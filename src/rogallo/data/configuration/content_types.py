"""Provides code for loading the list of displayable content types."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Local imports.
from ._io import load_configuration


##############################################################################
@cache
def load_displayable_content_types() -> list[str]:
    """Load the list of displayable content types.

    Returns:
        The loaded list of displayable content types.
    """
    return load_configuration("displayable-content-types", default=[])


### content_types.py ends here
