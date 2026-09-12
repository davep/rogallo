"""Provides utility functions for presenting information to the user."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Port70 imports.
from port70 import GopherURI

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Port1900 imports.
from port1900 import NexURI

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Wasat imports.
from wasat import GeminiURI, TitanURI
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from .types import RogalloLocation


##############################################################################
def short_path(path: Path) -> Path:
    """Get a short path representation of a path.

    Args:
        path: The path to get a short representation of.

    Returns:
        A short path representation of the path.
    """
    try:
        return Path("~") / path.relative_to(Path.home())
    except ValueError:
        return path


##############################################################################
def short_location(location: RogalloLocation) -> str:
    """Get a short string representation of a location.

    Args:
        location: The location to get a short string representation of.

    Returns:
        A short string representation of the location.
    """
    if isinstance(location, (FingerURI, GopherURI, SpartanURI, NexURI, TitanURI)):
        return str(location)
    if isinstance(location, GeminiURI):
        return str(location).removeprefix(GEMINI_PREFIX)
    return short_path(location).as_posix()


### presentation.py ends here
