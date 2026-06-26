"""Functions for testing locations."""

##############################################################################
# Python imports.
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

##############################################################################
# Wasat imports.
from wasat import GeminiURI, URIError

##############################################################################
# Local imports.
from .types import GEMINI_EXTENSIONS, GEMINI_MIME_TYPE

##############################################################################
# Add Gemini MIME types to the mimetypes module.
for extension in GEMINI_EXTENSIONS:
    mimetypes.add_type(GEMINI_MIME_TYPE, extension)


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

    Raises:
        ValueError: If the URI can't be turned into a [`Path`][pathlib.Path].
    """

    if (parsed := urlparse(uri)).scheme.lower() == "file":
        return Path(parsed.path).resolve()
    elif not parsed.scheme and not parsed.netloc:
        return Path(uri).expanduser().resolve()
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


##############################################################################
def is_likely_text_file(uri: str) -> bool:
    """Determine if a URI is likely a text file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a text file, `False` otherwise.
    """
    if not is_likely_local_file(uri):
        return False
    try:
        mime_type, _ = mimetypes.guess_type(path_from_uri(uri))
    except ValueError:
        return False
    return mime_type is not None and mime_type.startswith("text/")


### location_tests.py ends here
