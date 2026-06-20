"""Functions for testing locations."""

##############################################################################
# Python imports.
from urllib.parse import urlparse

##############################################################################
# Wasat imports.
from wasat import GeminiURI, URIError


##############################################################################
def is_likely_page_relative(uri: str) -> bool:
    """Determine if a URI is likely a relative URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a relative URI, `False` otherwise.
    """
    return not urlparse(uri).scheme


##############################################################################
def is_likely_capsule(uri: str) -> bool:
    """Determine if a URI is likely a capsule.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a capsule, `False` otherwise.
    """
    try:
        # Check if it's a straight-up Gemini URI.
        _ = GeminiURI(uri)
        return True
    except URIError:
        # If it's not, check if it's likely a relative URI.
        return is_likely_page_relative(uri)


### location_tests.py ends here
