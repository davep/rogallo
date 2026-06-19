"""Functions for testing locations."""

##############################################################################
# Python imports.
from urllib.parse import urlparse

##############################################################################
# Wasat imports.
from wasat import GeminiURI, URIError


##############################################################################
def is_likely_capsule(uri: str) -> bool:
    """Determine if a URI is likely a capsule.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a capsule, `False` otherwise.
    """

    # Check if it's a straight-up Gemini URI.
    try:
        _ = GeminiURI(uri)
        return True
    except URIError:
        # If it has a scheme at this point, it's not a capsule.
        return not urlparse(uri).scheme


### location_tests.py ends here
