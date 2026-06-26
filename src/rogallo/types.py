"""Application-wide types."""

##############################################################################
# Python imports.
from pathlib import Path
from typing import Final

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
type GeminiLocation = Path | GeminiURI
"""The type of a location from Gemini content."""

##############################################################################
GEMINI_MIME_TYPE: Final[str] = "text/gemini"
"""The MIME type for Gemini content."""

##############################################################################
GEMINI_EXTENSIONS: Final[set[str]] = {".gmi", ".gmni", ".gemini"}
"""The set of file extensions for Gemini content."""

### types.py ends here
