"""Provides the class that holds a Gemini document."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# Local imports.
from .types import GeminiLocation, is_gemini_mime_type


##############################################################################
class Document(NamedTuple):
    """A named tuple representing details of the document."""

    location: GeminiLocation | None = None
    """The source of the document.

    Note that this might not be the original location of the document if it
    was redirected from one location to another. For the original location
    of the document, see `original_location`.
    """

    original_location: GeminiLocation | None = None
    """The original source of the document, if any.

    This will differ from the location if the document was redirected from
    one location to another.
    """

    content: str = ""
    """The content of the document."""

    mime_type: str | None = None
    """The MIME type of the document, if any."""

    from_cache: bool = False
    """Whether the document was loaded from cache."""

    needed_certificate: bool = False
    """Whether the document required a client certificate to access."""

    def __bool__(self) -> bool:
        """Return `True` if the document has content, `False` otherwise."""
        return bool(self.content)

    @property
    def is_gemtext(self) -> bool:
        """`True` if the document is a Gemtext document, `False` otherwise."""
        return is_gemini_mime_type(self.mime_type)


### document.py ends here
