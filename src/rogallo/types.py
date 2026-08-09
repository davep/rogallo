"""Application-wide types."""

##############################################################################
# Python imports.
from pathlib import Path
from typing import Final

##############################################################################
# Port70 imports.
from port70 import GopherURI

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Wasat imports.
from wasat import GeminiURI
from wasat.uri import GEMINI_PREFIX

##############################################################################
type RogalloLocation = Path | GeminiURI | FingerURI | GopherURI | SpartanURI
"""The type of a location handled by Rogallo."""

##############################################################################
GEMINI_MIME_TYPE: Final[str] = "text/gemini"
"""The MIME type for Gemini content."""

##############################################################################
DEFAULT_GEMINI_EXTENSION: Final[str] = ".gmi"
"""The default file extension for Gemini content."""

##############################################################################
GEMINI_EXTENSIONS: Final[set[str]] = {DEFAULT_GEMINI_EXTENSION, ".gmni", ".gemini"}
"""The set of file extensions for Gemini content."""


##############################################################################
class SpartanURINeedingData(SpartanURI):
    """A SpartanURI that requires data to be sent with the request."""


##############################################################################
def short_location(location: RogalloLocation) -> str:
    """Get a short string representation of a location.

    Args:
        location: The location to get a short string representation of.

    Returns:
        A short string representation of the location.
    """
    if isinstance(location, (FingerURI, GopherURI, SpartanURI)):
        return str(location)
    if isinstance(location, GeminiURI):
        return str(location).removeprefix(GEMINI_PREFIX)
    try:
        return (Path("~") / location.relative_to(Path.home())).as_posix()
    except ValueError:
        return location.as_posix()


### types.py ends here
