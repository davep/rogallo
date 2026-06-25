"""Functions for testing locations."""

##############################################################################
# Python imports.
from pathlib import Path
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


##############################################################################
def path_from_uri(uri: str) -> Path:
    """Get the path from a URI.

    Args:
        uri: The URI to get the path from.

    Returns:
        The path from the URI.
    """

    if (parsed := urlparse(uri)).scheme == "file":
        return Path(parsed.path)
    elif not parsed.scheme and not parsed.netloc:
        return Path(uri)
    raise ValueError(f"URI is not a local file: {uri}")


##############################################################################
def is_likely_local_file(uri: str) -> bool:
    """Determine if a URI is likely a local file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a local file, `False` otherwise.
    """
    try:
        candidate = path_from_uri(uri)
    except ValueError:
        return False
    return candidate.exists() and candidate.is_file()


### location_tests.py ends here
