"""Application-wide types."""

##############################################################################
# Python imports.
from pathlib import Path
from typing import Final

##############################################################################
# Wasat imports.
from wasat import GeminiURI
from wasat.uri import GEMINI_PREFIX

##############################################################################
type GeminiLocation = Path | GeminiURI
"""The type of a location from Gemini content."""

##############################################################################
GEMINI_MIME_TYPE: Final[str] = "text/gemini"
"""The MIME type for Gemini content."""

##############################################################################
GEMINI_EXTENSIONS: Final[set[str]] = {".gmi", ".gmni", ".gemini"}
"""The set of file extensions for Gemini content."""


##############################################################################
def short_location(location: GeminiLocation) -> str:
    """Get a short string representation of a location.

    Args:
        location: The location to get a short string representation of.

    Returns:
        A short string representation of the location.
    """
    if isinstance(location, GeminiURI):
        return str(location).removeprefix(GEMINI_PREFIX)
    try:
        return (Path("~") / location.relative_to(Path.home())).as_posix()
    except ValueError:
        return location.as_posix()


### types.py ends here
