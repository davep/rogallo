"""Provides the class that holds a Gemini document."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

##############################################################################
# Gophermap imports.
from gophermap import GopherMap

##############################################################################
# Port70 imports.
from port70 import GopherURI

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Wasat imports.
from wasat import ServerCertificate, VerificationMethod

##############################################################################
# Local imports.
from .mime_checks import is_gemini_mime_type, is_gopher_mime_type
from .types import RogalloLocation


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

    avoid_cache: bool = False
    """Whether the document should avoid being cached."""

    verification_method: VerificationMethod | None = None
    """The method used to verify the server, if any."""

    server_certificate: ServerCertificate | None = None
    """The server's certificate, if any."""

    def __bool__(self) -> bool:
        """Return `True` if the document has content, `False` otherwise."""
        return bool(self.content)

    @cached_property
    def mime_type_sans_parameters(self) -> str | None:
        """The MIME type cleaned of any parameters.."""
        if self.mime_type is None:
            return None
        mime_type, _, _ = self.mime_type.partition(";")
        return mime_type.strip().lower()

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
        return isinstance(self.location, GopherURI) and GopherMap.is_likely_error(
            self.content
        )

    @property
    def is_renderable_as_gemtext(self) -> bool:
        """`True` if the document is a source code document, `False` otherwise."""
        return self.is_gemtext or self.is_gophermap or self.is_gopher_error

    @cached_property
    def suggested_filename(self) -> str:
        """The suggested filename for the document, if any."""
        if (location := self.location) is None:
            return "index.txt"
        if isinstance(location, Path):
            return location.name or "index.txt"
        if isinstance(location, FingerURI):
            return f"{location.username}.txt"
        if location.path and not location.path.endswith("/"):
            return Path(location.path).name
        return "gophermap.txt" if isinstance(location, GopherURI) else "index.gmi"


### document.py ends here
