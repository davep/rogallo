"""Functions for testing locations."""

##############################################################################
# Python imports.
import mimetypes
from pathlib import Path
from typing import TypeGuard
from urllib.parse import urlparse

##############################################################################
# Port70 imports.
from port70 import GopherURI
from port70 import URIError as GopherURIError

##############################################################################
# Port79 imports.
from port79 import FingerURI
from port79 import URIError as FingerURIError

##############################################################################
# Port1900 imports.
from port1900 import NexURI
from port1900 import URIError as NexURIError

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI
from sybaritic import URIError as SpartanURIError

##############################################################################
# Wasat imports.
from wasat import GeminiURI, TitanURI
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
def is_gopher_uri(uri: str) -> bool:
    """Determine if a URI is a Gopher URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Gopher URI, `False` otherwise.
    """
    try:
        _ = GopherURI(uri)
    except GopherURIError:
        return False
    return True


##############################################################################
def is_spartan_uri(uri: str) -> bool:
    """Determine if a URI is a Spartan URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Spartan URI, `False` otherwise.
    """
    try:
        _ = SpartanURI(uri)
    except SpartanURIError:
        return False
    return True


##############################################################################
def is_nex_uri(uri: str) -> bool:
    """Determine if a URI is a Nex URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Nex URI, `False` otherwise.
    """
    try:
        _ = NexURI(uri)
    except NexURIError:
        return False
    return True


##############################################################################
def is_titan_uri(uri: str) -> bool:
    """Determine if a URI is a Titan URI.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a Titan URI, `False` otherwise.
    """
    try:
        _ = TitanURI(uri)
    except GeminiURIError:
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
    except GeminiURIError:
        # If it's not, check if it's likely a relative URI.
        return is_likely_page_relative(uri)
    return True


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
def is_likely_finger_request(text: str) -> bool:
    """Determine if some text is likely a Finger request.

    Args:
        text: The text to check.

    Returns:
        `True` if the text is likely a Finger request, `False` otherwise.
    """
    if "@" not in text:
        return False
    try:
        _ = FingerURI.from_string(text)
    except FingerURIError:
        return False
    return True


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
def local_index_from_uri(uri: str) -> Path:
    """Get the local index file from a URI.

    Args:
        uri: The URI to get the local index file from.

    Returns:
        The local index file from the URI.

    Note:
        If the URI is a local directory, this function will look for an index
        file with one of the known Gemini extensions. If it finds one, it will
        return that file. If it doesn't find one, it will return the directory
        itself.

    Raises:
        ValueError: If the URI is not a local directory.
    """
    if not is_local_directory(uri):
        raise ValueError(f"URI is not a local directory: {uri}")
    root = path_from_uri(uri)
    for extension in GEMINI_EXTENSIONS:
        if (candidate := (root / "index").with_suffix(extension)).is_file():
            return candidate
    return root


##############################################################################
def is_local_file(uri: str) -> bool:
    """Determine if a URI is a local file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a file, `False` otherwise.

    Notes:
        The URI is considered to be a local file if it can be turned into a
        [`Path`][pathlib.Path] and that path is a file that exists.
    """
    try:
        candidate = path_from_uri(uri)
    except ValueError:
        return False
    return candidate.is_file()


##############################################################################
def is_local_directory(uri: str) -> bool:
    """Determine if a URI is a local directory.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is likely a directory, `False` otherwise.

    Notes:
        The URI is considered to be a local directory if it can be turned into a
        [`Path`][pathlib.Path] and that path is a directory that exists.
    """
    try:
        candidate = path_from_uri(uri)
    except ValueError:
        return False
    return candidate.is_dir()


##############################################################################
def is_local_file_of_type(uri: str, mime_type: str) -> bool:
    """Determine if a URI is a local file of a given MIME type.

    Args:
        uri: The URI to check.
        mime_type: The MIME type to check for.

    Returns:
        `True` if the URI is likely a local text file, `False` otherwise.

    Notes:
        The URI is only considered to be a local file if it can be turned
        into a [`Path`][pathlib.Path] and that path is a file that exists,
        and the MIME type of that file starts with the given `mime_type`.
    """
    if not is_local_file(uri):
        return False
    try:
        guessed_mime_type, _ = mimetypes.guess_type(path_from_uri(uri))
    except ValueError:
        return False
    return guessed_mime_type is not None and guessed_mime_type.startswith(mime_type)


##############################################################################
def is_local_text_file(uri: str) -> bool:
    """Determine if a URI is local text file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a local text file, `False` otherwise.

    Notes:
        The URI is considered to be a local text file if it can be turned
        into a [`Path`][pathlib.Path] and that path is a file that exists,
        and the MIME type of that file starts with "text/".
    """
    return is_local_file_of_type(uri, "text/")


##############################################################################
def is_local_gemtext_file(uri: str) -> bool:
    """Determine if a URI is a local Gemtext file.

    Args:
        uri: The URI to check.

    Returns:
        `True` if the URI is a local Gemtext file, `False` otherwise.

    Notes:
        The URI is considered to be a local Gemtext file if it can be turned
        into a [`Path`][pathlib.Path] and that path is a file that exists
        and the MIME type comes back as the Gemini MIME type.
    """
    return is_local_file_of_type(uri, GEMINI_MIME_TYPE)


##############################################################################
def has_navigable_path(
    location: RogalloLocation | None,
) -> TypeGuard[GeminiURI | SpartanURI | NexURI | GopherURI]:
    """Determine if a location has a navigable path.

    Args:
        location: The location to check.

    Returns:
        `True` if the location has a navigable path, `False` otherwise.
    """
    return isinstance(location, (GeminiURI, SpartanURI, NexURI, GopherURI))


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
        if is_gopher_uri(str):
            return GopherURI(str)
        if is_spartan_uri(str):
            return SpartanURI(str)
        if is_nex_uri(str):
            return NexURI(str)
        return path_from_uri(str)
    except ValueError as error:
        raise ValueError(f"Cannot make location from string: {str}") from error


### location_tests.py ends here
