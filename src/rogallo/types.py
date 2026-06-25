"""Application-wide types."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
type GeminiLocation = Path | GeminiURI
"""The type of a location from Gemini content."""

### types.py ends here
