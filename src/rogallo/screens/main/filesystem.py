"""Provides code for handling a filesystem request."""

##############################################################################
# Python imports.
from mimetypes import guess_type
from pathlib import Path

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...document import Document
from ...messages import OpenLocation
from ...mime_checks import is_displayable_mime_type
from .local_messages import OpenDocument, OpenUnsupportedMIMEType


##############################################################################
def handle_filesystem_request(request: OpenLocation, owner: Widget) -> None:
    """Handle a filesystem request.

    Args:
        request: The filesystem request to handle.
        owner: The widget that owns the request.
    """
    uri = request.location
    assert isinstance(uri, Path)

    mime_type = guess_type(uri)[0] or "application/octet-stream"
    if not is_displayable_mime_type(mime_type):
        owner.post_message(OpenUnsupportedMIMEType(uri, mime_type))
        return

    try:
        owner.post_message(
            OpenDocument(
                document=Document(
                    location=request.location,
                    original_location=request.location,
                    content=uri.read_text(encoding="utf-8"),
                    mime_type=mime_type,
                ),
                original_request=request,
            )
        )
    except OSError as error:
        owner.notify(
            f"Error loading {request.location}:\n\n{error}",
            severity="error",
            title="Filesystem Error",
        )
    except UnicodeDecodeError as error:
        owner.notify(
            f"Error loading {request.location}:\n\n{error}\n\nLikely not a text file.",
            severity="error",
            title="Decode Error",
        )


### filesystem.py ends here
