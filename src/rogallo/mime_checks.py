"""Provides functions for checking MIME types."""

##############################################################################
# Python imports.
from functools import cache

##############################################################################
# Gophermap imports.
from gophermap import ItemType

##############################################################################
# Local imports.
from .data import load_configuration
from .types import GEMINI_MIME_TYPE


##############################################################################
@cache
def is_gemini_mime_type(mime_type: str | None) -> bool:
    """Check if a MIME type is a Gemini MIME type.

    Args:
        mime_type: The MIME type to check.

    Returns:
        True if the MIME type is a Gemini MIME type, False otherwise.
    """
    return mime_type is not None and mime_type.startswith(GEMINI_MIME_TYPE)


##############################################################################
@cache
def is_gopher_mime_type(mime_type: str | None) -> bool:
    """Check if a MIME type is a Gopher MIME type.

    Args:
        mime_type: The MIME type to check.

    Returns:
        True if the MIME type is a Gopher MIME type, False otherwise.
    """
    return mime_type is not None and mime_type.startswith(
        (
            ItemType.MENU.mime_type,
            ItemType.INDEX_SEARCH.mime_type,
        )
    )


##############################################################################
@cache
def is_displayable_mime_type(mime_type: str | None) -> bool:
    """Check if a MIME type is displayable in Rogallo.

    Args:
        mime_type: The MIME type to check.

    Returns:
        `True` if the MIME type is displayable, `False` otherwise.
    """
    if mime_type is None:
        return False
    mime_type, _, _ = mime_type.partition(";")
    return mime_type.startswith("text/") or mime_type in {
        ItemType.MENU.mime_type,
        ItemType.INDEX_SEARCH.mime_type,
        *load_configuration().displayable_content_types,
    }


### mime_checks.py ends here
