"""Provides code for handling a gopher request."""

##############################################################################
# Gophermap imports.
from gophermap import ItemType

##############################################################################
# Port70 imports.
from port70 import Client, GopherURI, Port70Error

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.dialogs import ModalInput

##############################################################################
# Local imports.
from ...cache import ContentCache
from ...document import Document
from ...messages import OpenLocation
from ...mime_checks import is_displayable_mime_type
from .local_messages import OpenDocument, OpenUnsupportedMIMEType


##############################################################################
async def handle_gopher_request(
    request: OpenLocation,
    current_document: Document,
    client: Client,
    owner: Widget,
    cache: ContentCache,
) -> None:
    """Handle a gopher request.

    Args:
        request: The gopher request to handle.
        current_document: The current document being viewed.
        client: The client to use for the request.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
    """
    uri = request.location
    assert isinstance(uri, GopherURI)

    # If it's a search and we don't know what we're looking for, ask the
    # user what they want to search for.
    if ItemType(uri.item_type) is ItemType.INDEX_SEARCH and uri.query is None:
        if search_query := await owner.app.push_screen_wait(
            ModalInput(
                title=f"Search {uri.host}:{uri.port}",
                initial=(
                    current_document.location.query or ""
                    if isinstance(current_document.location, GopherURI)
                    else ""
                ),
            )
        ):
            uri = uri.with_query(search_query)
        else:
            return

    # If a cached copy of the document exists and the request allows it,
    # use that instead of making a network request.
    if (
        ItemType(uri.item_type) is not ItemType.INDEX_SEARCH
        and request.allow_cached
        and (
            cached_document := cache.get_document(
                uri, avoid_history=request.avoid_history
            )
        )
    ):
        owner.post_message(OpenDocument(cached_document))
        return

    # While Gopher doesn't deal with MIME types, Rogallo does for the
    # most part, so let's figure out the effective MIME type for what
    # we're doing here.
    mime_type = ItemType(uri.item_type).mime_type
    if not is_displayable_mime_type(mime_type):
        owner.post_message(OpenUnsupportedMIMEType(uri, mime_type))
        return

    try:
        owner.post_message(
            OpenDocument(
                cache.add_document(
                    Document(
                        location=uri,
                        original_location=uri,
                        content=(await client.request(uri)).text,
                        mime_type=mime_type,
                        avoid_cache=ItemType(uri.item_type) is ItemType.INDEX_SEARCH,
                        avoid_history=request.avoid_history,
                    )
                )
            )
        )
    except Port70Error as error:
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Gopher Error",
        )


### gopher.py ends here
