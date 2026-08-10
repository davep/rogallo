"""Provides code for handling a finger request."""

##############################################################################
# Port79 imports.
from port79 import Client, FingerURI, Port79Error

##############################################################################
# Textual imports.
from textual.screen import Screen

##############################################################################
# Local imports.
from ...document import Document
from ...messages import OpenLocation
from .local_messages import OpenDocument


##############################################################################
async def handle_finger_request(
    request: OpenLocation, client: Client, screen: Screen[None]
) -> None:
    """Handle a finger request.

    Args:
        request: The finger request to handle.
        client: The client to use for the request.
        screen: The screen to post the document to.
    """
    uri = request.location
    assert isinstance(uri, FingerURI)

    try:
        screen.post_message(
            OpenDocument(
                document=Document(
                    location=uri,
                    original_location=uri,
                    content=(await client.request(uri)).text,
                    mime_type="text/plain",
                ),
                original_request=request,
            )
        )
    except Port79Error as error:
        screen.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Finger Error",
        )


### finger.py ends here
