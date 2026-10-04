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
from ....messages import AcquireLocation, DownloadLocation, OpenLocation
from ..local_messages import OpenDocument


##############################################################################
async def _open_document(
    uri: FingerURI,
    request: OpenLocation,
    client: Client,
    cache: ContentCache,
    owner: Widget,
) -> None:
    """Open a document from a finger request.

    Args:
        uri: The URI to open.
        request: The open location request.
        client: The client to use for the request.
        cache: The content cache to use for caching documents.
        owner: The widget that owns the request.
    """
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


##############################################################################
async def _download_document(
    uri: FingerURI, request: DownloadLocation, client: Client, owner: Widget
) -> None:
    """Download a document from a finger request.

    Args:
        uri: The URI to download.
        request: The download location request.
        client: The client to use for the request.
        owner: The widget that owns the request.
    """
    request.target.write_bytes((await client.request(uri)).raw_bytes)
    owner.notify(f"Downloaded {uri} to {request.target}", title="Download Complete")


##############################################################################
async def handle_finger_request(
    request: AcquireLocation, client: Client, owner: Widget, cache: ContentCache
) -> None:
    """Handle a finger request.

    Args:
        request: The finger request to handle.
        client: The client to use for the request.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
    """
    uri = request.location
    assert isinstance(uri, FingerURI)

    # Check the cache first.
    if (
        isinstance(request, OpenLocation)
        and request.allow_cached
        and (
            cached_document := cache.get_document(
                uri, avoid_history=request.avoid_history
            )
        )
    ):
        owner.post_message(
            OpenDocument(cached_document, from_history=request.from_history)
        )
        return

    try:
        if isinstance(request, OpenLocation):
            await _open_document(uri, request, client, cache, owner)
        else:
            await _download_document(uri, request, client, owner)
    except Port79Error as error:
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Finger Error",
        )


### finger.py ends here
