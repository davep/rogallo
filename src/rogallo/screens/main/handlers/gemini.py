"""Provides code for handling a Gemini request."""

##############################################################################
# Python imports.
from collections.abc import Callable

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import (
    Client,
    ConnectionError,
    GeminiURI,
    Response,
    SecurityError,
    StatusCode,
    URIError,
)

##############################################################################
# Local imports.
from ....cache import ContentCache
from ....document import Document
from ....input_content import InputContent
from ....messages import OpenLocation
from ....mime_checks import is_displayable_mime_type
from ...certificate import Certificate
from ...user_input import UserInput
from ..local_messages import OpenDocument, OpenUnsupportedMIMEType
from .text_decoder import decode_text

##############################################################################
type LastInputSetter = Callable[[InputContent | None], None]
"""Type of a setter for the last input."""
type LastInputGetter = Callable[[], InputContent | None]
"""Type of a getter for the last input."""


##############################################################################
async def _handle_client_certificate_request(
    location: GeminiURI, request_reason: str, client: Client, owner: Widget
) -> None:
    """Handle a request for a client certificate from a Gemini request.

    Args:
        location: The location making the request.
        request_reason: The reason for the client certificate request.
        client: The client to use for the request.
        owner: The widget that owns the request.
    """

    if (
        certificate_data := await owner.app.push_screen_wait(
            Certificate(location, request_reason)
        )
    ) is None:
        owner.notify("Client certificate request cancelled.", severity="warning")
        return

    try:
        await client.client_cert_store.create_credentials(**certificate_data)
    except (ValueError, OSError, RuntimeError) as error:
        owner.notify(
            f"Unable to create client certificate for {location}:\n\n{error}",
            severity="error",
            title="Client Certificate Error",
        )
        return
    owner.post_message(OpenLocation(location, allow_cached=False))


##############################################################################
async def _handle_input_request(
    location: GeminiURI,
    prompt: str,
    sensitive: bool,
    owner: Widget,
    get_last_input: LastInputGetter,
) -> None:
    """Handle a request for input from a Gemini request.

    Args:
        location: The location making the request.
        prompt: The prompt to display to the user.
        sensitive: Whether the input is sensitive.
        owner: The widget that owns the request.
        get_last_input: A function to get the last input from the user.
    """
    initial_input = ""
    if ((last_input := get_last_input()) is not None) and last_input == InputContent(
        location=location, prompt=prompt, sensitive=sensitive
    ):
        initial_input = last_input.content
    if user_input := await owner.app.push_screen_wait(
        UserInput(location, prompt=prompt, sensitive=sensitive, default=initial_input)
    ):
        try:
            owner.post_message(
                OpenLocation(
                    location=location.with_query(user_input),
                    allow_cached=False,
                    associated_input=InputContent(
                        location=location,
                        prompt=prompt,
                        sensitive=sensitive,
                        content=user_input,
                    ),
                )
            )
        except URIError as error:
            owner.notify(
                f"Unable to create query for {location}:\n\n{error}",
                severity="error",
                title="Input Error",
            )


##############################################################################
async def _handle_response(
    response: Response,
    request: OpenLocation,
    client: Client,
    owner: Widget,
    cache: ContentCache,
    set_last_input: LastInputSetter,
    get_last_input: LastInputGetter,
) -> None:
    """Handle a response from a Gemini request.

    Args:
        response: The response to handle.
        request: The original request that generated the response.
        client: The client to use for the request.
        owner: The widget that owns the request.
        cache: The content cache to use for caching documents.
        set_last_input: A function to set the last input from the user.
        get_last_input: A function to get the last input from the user.
    """
    assert isinstance(request.location, GeminiURI)
    uri = response.uri or response.requested_uri or request.location

    # Handle a request for user input.
    if response.status.is_input:
        await _handle_input_request(
            uri,
            response.meta.strip(),
            response.status is StatusCode.SENSITIVE_INPUT,
            owner,
            get_last_input,
        )
        return

    # Handle a request for a client certificate.
    if response.status.is_client_certificate_required:
        await _handle_client_certificate_request(
            uri, response.meta.strip(), client, owner
        )
        return

    # Handle any other non-successful response.
    if not response.status.is_success:
        set_last_input(request.associated_input)
        owner.notify(
            f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
            severity="error",
            title="Request Error",
        )
        return

    # Clear out any saved input.
    set_last_input(None)

    # Handle a successful response.
    if is_displayable_mime_type(response.mime_type):
        owner.post_message(
            OpenDocument(
                cache.add_document(
                    Document(
                        location=uri,
                        original_location=request.location,
                        content=await decode_text(response),
                        mime_type=response.mime_type,
                        needed_certificate=response.client_cert_used,
                        verification_method=response.verification_method,
                        server_certificate=response.server_cert,
                        avoid_cache=response.client_cert_used,
                        avoid_history=request.avoid_history,
                    )
                ),
                from_history=request.from_history,
            )
        )
    else:
        owner.post_message(OpenUnsupportedMIMEType(uri, response.mime_type))


##############################################################################
async def handle_gemini_request(
    request: OpenLocation,
    owner: Widget,
    client: Client,
    cache: ContentCache,
    set_last_input: LastInputSetter,
    get_last_input: LastInputGetter,
) -> None:
    """Handle a Gemini request.

    Args:
        request: The Gemini request to handle.
        owner: The widget that owns the request.
        client: The client to use for the request.
        cache: The content cache to use for caching documents.
        set_last_input: A function to set the last input from the user.
        get_last_input: A function to get the last input from the user.
    """

    uri = request.location
    assert isinstance(uri, GeminiURI)

    # If a cached copy of the document exists and the request allows it,
    # use that instead of making a network request.
    if (
        request.allow_cached
        and (
            cached_document := cache.get_document(
                uri, avoid_history=request.avoid_history
            )
        )
        is not None
    ):
        owner.post_message(
            OpenDocument(document=cached_document, from_history=request.from_history)
        )
        return

    # Otherwise, make a request to the capsule and handle the response.
    try:
        async with await client.request(uri) as response:
            await _handle_response(
                response, request, client, owner, cache, set_last_input, get_last_input
            )
    except ConnectionError as error:
        set_last_input(request.associated_input)
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Connection Error",
        )
    except SecurityError as error:
        owner.notify(
            f"Error loading {uri}:\n\n{error}",
            severity="error",
            title="Security Error",
        )


### gemini.py ends here
