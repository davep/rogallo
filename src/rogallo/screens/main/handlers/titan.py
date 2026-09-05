"""Provides code for handling a Titan request."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import (
    Client,
    ConnectionError,
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
from ....input_content import InputContent
from ....messages import OpenLocation
from ....mime_checks import is_displayable_mime_type
from ....text_decoder import decode_text
from ...user_upload import UserUpload
from ..local_messages import OpenDocument, OpenUnsupportedMIMEType
from ._glv import (
    LastInputGetter,
    LastInputSetter,
    document,
    handle_client_certificate_request,
    handle_security_error,
)


##############################################################################
async def _handle_response(
    response: Response,
    request: OpenLocation,
    client: Client,
    owner: Widget,
    set_last_input: LastInputSetter,
    savable_input: InputContent | None = None,
) -> None:
    """Handle a Titan response.

    Args:
        response: The response to handle.
        request: The request that was made.
        client: The Titan client to use for any follow-up requests.
        owner: The widget that owns the request.
        set_last_input: A function to set the last input from the user.
    """
    uri = response.uri or response.requested_uri or request.location
    assert isinstance(uri, GeminiURI | TitanURI)

    # Handle a request for a client certificate.
    if response.status.is_client_certificate_required:
        set_last_input(savable_input)
        await handle_client_certificate_request(
            uri, response.meta.strip(), client, owner
        )
        return

    # Handle any other non-successful response.
    if not response.status.is_success:
        set_last_input(savable_input)
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
                await document(uri, request, response),
                from_history=request.from_history,
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
        await handle_security_error(client, error, uri, owner)
    return None


##############################################################################
async def handle_titan_request(
    request: OpenLocation,
    owner: Widget,
    client: Client,
    set_last_input: LastInputSetter,
    get_last_input: LastInputGetter,
) -> None:
    """Handle a Titan request.

    Args:
        request: The request to handle.
        owner: The widget that owns the request.
        client: The Titan client to use for the request.
    """

    uri = request.location
    assert isinstance(uri, TitanURI)

    # Set up the initial input. If there is a last input that matches the
    # current request, use that as the initial input.
    initial_input = ""
    if ((last_input := get_last_input()) is not None) and last_input == InputContent(
        location=uri, prompt=""
    ):
        initial_input = last_input.content

    # If it's a Titan request that is a request to edit existing content,
    # get the existing content before edit, and also override any saved
    # content from a previous error.
    if uri.is_edit:
        if (
            raw_from_server := await _get_raw_content_to_edit(uri, client, owner)
        ) is None:
            return
        initial_input = raw_from_server

    # Prompt the user for what they want to upload, and then upload it.
    if upload := await owner.app.push_screen_wait(UserUpload(uri, initial_input)):
        savable_input = (
            InputContent(location=uri, prompt="", content=upload.data)
            if isinstance(upload.data, str)
            else None
        )
        try:
            async with await client.upload(
                uri=uri,
                data=upload.data,
                mime=upload.mime_type,
                token=upload.token,
            ) as response:
                await _handle_response(
                    response, request, client, owner, set_last_input, savable_input
                )
        except (
            URIError,
            ConnectionError,
            ProtocolError,
            RedirectError,
            TypeError,
        ) as error:
            if savable_input:
                set_last_input(savable_input)
            owner.notify(
                f"Error loading {uri}:\n\n{error}",
                severity="error",
                title="Connection Error",
            )
        except SecurityError as error:
            await handle_security_error(client, error, uri, owner)


### titan.py ends here
