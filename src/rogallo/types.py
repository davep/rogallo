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
# Port1900 imports.
from port1900 import NexURI

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
type RogalloLocation = Path | GeminiURI | FingerURI | GopherURI | SpartanURI | NexURI
"""The type of a location handled by Rogallo."""

##############################################################################
SUPPORTED_PROTOCOLS: Final[tuple[str, ...]] = (
    "file",
    "finger",
    "gemini",
    "gopher",
    "nex",
    "spartan",
)
"""The set of protocols handled by Rogallo."""

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


### types.py ends here
