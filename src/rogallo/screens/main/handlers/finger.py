"""Provides code for handling a finger request."""

##############################################################################
# Port79 imports.
from port79 import Client, FingerURI, Port79Error

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ....cache import ContentCache
from ....document import Document
from ....messages import OpenLocation
from ..local_messages import OpenDocument


##############################################################################
async def handle_finger_request(
    request: OpenLocation, client: Client, owner: Widget, cache: ContentCache
) -> None:
    """Handle a finger request.

    Args:
        request: The finger request to handle.
        client: The client to use for the request.
        screen: The screen to post the document to.
        cache: The content cache to use for caching documents.
    """
    uri = request.location
    assert isinstance(uri, FingerURI)

    # Check the cache first.
    if request.allow_cached and (
        cached_document := cache.get_document(uri, avoid_history=request.avoid_history)
    ):
        owner.post_message(
            OpenDocument(cached_document, from_history=request.from_history)
        )
        return

    try:
        owner.post_message(
            OpenDocument(
                cache.add_document(
                    Document(
                        location=uri,
                        original_location=uri,
                        content=(await client.request(uri)).text,
                        mime_type="text/plain",
                        avoid_cache=False,
                        avoid_history=request.avoid_history,
                    )
                ),
                from_history=request.from_history,
            )
        )
    except Port79Error as error:
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Finger Error",
        )


### finger.py ends here
