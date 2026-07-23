"""Functions for testing locations."""

##############################################################################
# Python imports.
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

##############################################################################
# Port97 imports.
from port79 import FingerURI
from port79 import URIError as FingerURIError

##############################################################################
# Wasat imports.
from wasat import GeminiURI
from wasat import URIError as GeminiURIError
from wasat.uri import GEMINI_PREFIX

##############################################################################
# Local imports.
from .types import GEMINI_EXTENSIONS, GEMINI_MIME_TYPE, RogalloLocation

##############################################################################
# Add Gemini MIME types to the mimetypes module.
for extension in GEMINI_EXTENSIONS:
    mimetypes.add_type(GEMINI_MIME_TYPE, extension)


##############################################################################
def is_gemini_uri(uri: str) -> bool:
    """Determine if a URI is a Gemini URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Gemini URI, `False` otherwise.
    """
    try:
        _ = GeminiURI(uri)
    except GeminiURIError:
        return False
    return True


##############################################################################
def is_finger_uri(uri: str) -> bool:
    """Determine if a URI is a Finger URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Finger URI, `False` otherwise.
    """
    try:
        _ = FingerURI(uri)
    except FingerURIError:
        return False
    return True


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
    except GeminiURIError:
        # If it's not, check if it's likely a relative URI.
        return is_likely_page_relative(uri)


##############################################################################
def is_likely_schemeless_capsule(uri: str) -> bool:
    """Determine if a URI is likely a schemeless capsule.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a schemeless capsule, `False` otherwise.
    """
    if urlparse(uri).scheme:
        return False
    return is_likely_capsule(f"{GEMINI_PREFIX}{uri}")


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
    return candidate.is_file()


##############################################################################
def is_likely_local_text_file(uri: str) -> bool:
    """Determine if a URI is likely a local text file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a local text file, `False` otherwise.
    """
    if not is_likely_local_file(uri):
        return False
    try:
        mime_type, _ = mimetypes.guess_type(path_from_uri(uri))
    except ValueError:
        return False
    return mime_type is not None and mime_type.startswith("text/")


##############################################################################
def make_location(str: str) -> RogalloLocation:
    """Make a location object from a string.

    Args:
        str: The string to make a location from.

    Returns:
        A location object.

    Raises:
        ValueError: If the string can't be turned into a location object.
    """
    try:
        if is_gemini_uri(str):
            return GeminiURI(str)
        if is_finger_uri(str):
            return FingerURI(str)
        return path_from_uri(str)
    except ValueError as error:
        raise ValueError(f"Cannot make location from string: {str}") from error


### location_tests.py ends here
