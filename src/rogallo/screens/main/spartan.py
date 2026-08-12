"""Provides code for handling a Spartan request."""

##############################################################################
# Sybaritic imports.
from sybaritic import Client, Response, SpartanURI, SybariticError

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...cache import ContentCache
from ...document import Document
from ...messages import OpenLocation
from ...mime_checks import is_displayable_mime_type
from ...types import SpartanURINeedingData
from ..user_input import UserInput
from .local_messages import OpenDocument, OpenUnsupportedMIMEType
from .text_decoder import decode_text


##############################################################################
async def _handle_response(
    response: Response, request: OpenLocation, owner: Widget, cache: ContentCache
) -> None:
    """Handle a response from a Spartan request.

    Args:
        response: The response to handle.
        request: The original request that generated the response.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
    """
    assert isinstance(request.location, SpartanURI)
    uri = response.uri or response.requested_uri or request.location

    # Handle any non-successful response.
    if not response.status.is_success:
        owner.notify(
            f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
            severity="error",
            title="Request Error",
        )
        return

    # Handle a successful response.
    if is_displayable_mime_type(response.mime_type):
        owner.post_message(
            OpenDocument(
                document=cache.add_document(
                    Document(
                        location=uri,
                        original_location=request.location,
                        content=await decode_text(response),
                        mime_type=response.mime_type,
                        avoid_cache=isinstance(uri, SpartanURINeedingData),
                    )
                ),
                original_request=request,
            )
        )
    else:
        owner.post_message(OpenUnsupportedMIMEType(uri, response.mime_type))


##############################################################################
async def handle_spartan_request(
    request: OpenLocation, client: Client, owner: Widget, cache: ContentCache
) -> None:
    """Handle a Spartan request.

    Args:
        request: The Spartan request to handle.
        client: The client to use for the request.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
    """

    uri = request.location
    assert isinstance(uri, SpartanURI)

    # If a cached copy of the document exists and the request allows it,
    # use that instead of making a network request.
    if (
        not isinstance(uri, SpartanURINeedingData)
        and request.allow_cached
        and (cached_document := cache.get_document(uri))
    ):
        owner.post_message(
            OpenDocument(
                document=cached_document,
                original_request=request,
            )
        )
        return

    # If we're looking at a Spartan request that needs data. Let's ask
    # the user for it.
    attached_data: str | None = None
    if isinstance(uri, SpartanURINeedingData) and not (
        attached_data := await owner.app.push_screen_wait(
            UserInput(uri, prompt="Spartan request requires data")
        )
    ):
        return

    try:
        async with await client.request(uri, data=attached_data) as response:
            await _handle_response(response, request, owner, cache)
    except SybariticError as error:
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Spartan Error",
        )


### spartan.py ends here
