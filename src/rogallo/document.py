"""Provides the class that holds a Gemini document."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import cached_property

##############################################################################
# Gophermap imports.
from gophermap import GopherMap, ItemType

##############################################################################
# Local imports.
from .types import RogalloLocation, is_gemini_mime_type, is_gopher_mime_type


##############################################################################
@dataclass(frozen=True)
class Document:
    """A named tuple representing details of the document."""

    location: RogalloLocation | None = None
    """The source of the document.

    Note that this might not be the original location of the document if it
    was redirected from one location to another. For the original location
    of the document, see `original_location`.
    """

    original_location: RogalloLocation | None = None
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

    @property
    def is_gophermap(self) -> bool:
        """`True` if the document is a Gophermap document, `False` otherwise."""
        return is_gopher_mime_type(self.mime_type)

    @cached_property
    def is_gopher_error(self) -> bool:
        """`True` if the document is a Gopher error document, `False` otherwise."""
        return ItemType.ERROR in {item.type for item in GopherMap(self.content).items}

    @property
    def is_source(self) -> bool:
        """`True` if the document is a source code document, `False` otherwise."""
        return self.is_gemtext or self.is_gophermap or self.is_gopher_error


### document.py ends here
