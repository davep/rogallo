"""Provides code for handling a Titan request."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import (
    Client,
    GeminiURI,
    ProtocolError,
    RedirectError,
    Response,
    SecurityError,
    TitanURI,
    URIError,
)

##############################################################################
# Local imports.
from ....document import Document
from ....messages import OpenLocation
from ....mime_checks import is_displayable_mime_type
from ....text_decoder import decode_text
from ...user_upload import UserUpload
from ..local_messages import OpenDocument, OpenUnsupportedMIMEType


##############################################################################
async def _handle_response(
    response: Response, request: OpenLocation, owner: Widget
) -> None:
    """Handle a Titan response.

    Args:
        response: The response to handle.
        owner: The widget that owns the request.
    """
    uri = response.uri or response.requested_uri or request.location
    assert isinstance(uri, GeminiURI | TitanURI)

    # TODO: Should I still handle a `is_client_certificate_required`
    # response here?

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
                Document(
                    location=uri,
                    original_location=request.location,
                    content=await decode_text(response),
                    mime_type=response.mime_type,
                    needed_client_certificate=response.client_cert_used,
                    client_certificate=response.client_cert,
                    verification_method=response.verification_method,
                    server_certificate=response.server_cert,
                    avoid_cache=response.client_cert_used,
                    avoid_history=request.avoid_history,
                )
            )
        )
    else:
        owner.post_message(OpenUnsupportedMIMEType(uri, response.mime_type))


##############################################################################
async def _get_raw_content_to_edit(
    uri: TitanURI, client: Client, owner: Widget
) -> str | None:
    """Get the raw content of a Titan document to edit.

    Args:
        uri: The URI of the document to edit.
        client: The Titan client to use for the request.
        owner: The widget that owns the request.

    Returns:
        The raw content of the document, or `None` if there was an error.
    """
    try:
        async with await client.edit(uri) as response:
            if not response.status.is_success:
                owner.notify(
                    f"Error loading {uri}:\n\n{response.status.value} {response.status.name}\n{response.meta}",
                    severity="error",
                    title="Request Error",
                )
                return None
            return await decode_text(response)
    except (
        URIError,
        ConnectionError,
        ProtocolError,
        RedirectError,
        ValueError,
        OSError,
        RuntimeError,
    ) as error:
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
    return None


##############################################################################
async def handle_titan_request(
    request: OpenLocation, owner: Widget, client: Client
) -> None:
    """Handle a Titan request.

    Args:
        request: The request to handle.
        owner: The widget that owns the request.
        client: The Titan client to use for the request.
    """

    uri = request.location
    assert isinstance(uri, TitanURI)

    # If it's a Titan request that is a request to edit existing content,
    # get the existing content first.
    raw_content = ""
    if uri.is_edit:
        if (
            raw_from_server := await _get_raw_content_to_edit(uri, client, owner)
        ) is None:
            return
        raw_content = raw_from_server

    # Prompt the user for what they want to upload, and then upload it.
    if upload := await owner.app.push_screen_wait(UserUpload(uri, raw_content)):
        try:
            async with await client.upload(
                uri=uri,
                data=upload.data,
                mime=upload.mime_type,
                token=upload.token,
            ) as response:
                await _handle_response(response, request, owner)
        except ConnectionError as error:
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


### titan.py ends here
