"""Provides code for handling a Nex request."""

##############################################################################
# Port1900 imports.
from port1900 import Client, NexURI, Port1900Error

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...cache import ContentCache
from ...document import Document
from ...messages import OpenLocation
from ...mime_checks import is_displayable_mime_type
from .local_messages import OpenDocument, OpenUnsupportedMIMEType


##############################################################################
async def handle_nex_request(
    request: OpenLocation, client: Client, owner: Widget, cache: ContentCache
) -> None:
    """Handle a Nex request.

    Args:
        request: The Nex request to handle.
        client: The client to use for the request.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
    """
    uri = request.location
    assert isinstance(uri, NexURI)

    # Check the cache first.
    if request.allow_cached and (
        cached_document := cache.get_document(uri, avoid_history=request.avoid_history)
    ):
        owner.post_message(OpenDocument(cached_document))
        return

    # Grab the data from the server.
    try:
        response = await client.request(uri)
    except Port1900Error as error:
        owner.notify(
            str(error),
            severity="error",
            title="Nex Error",
        )
        return

    # Don't show anything if the response itself was empty.
    if not response.text:
        owner.notify(
            f"No content returned from {uri}",
            severity="warning",
            title="Nex Warning",
        )
        return

    # Try and show it.
    if is_displayable_mime_type(response.mime_type):
        owner.post_message(
            OpenDocument(
                cache.add_document(
                    Document(
                        location=uri,
                        original_location=uri,
                        content=response.text,
                        mime_type=response.mime_type,
                        avoid_cache=False,
                        avoid_history=request.avoid_history,
                    )
                )
            )
        )
    else:
        owner.post_message(OpenUnsupportedMIMEType(uri, response.mime_type))


### nex.py ends here
