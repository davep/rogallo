"""Protocol handler code shared between Gemini and Titan."""

##############################################################################
# Python imports.
from collections.abc import Callable

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import AnyURI, Client, ClientCertificate, Response, SecurityError

##############################################################################
# Local imports.
from ....document import Document
from ....input_content import InputContent
from ....messages import ClientCertificatesModified, OpenLocation
from ....text_decoder import decode_text
from ...client_certificate import (
    CertificateData,
    ClientCertificatePicker,
    ClientCertificatePickerResult,
    LocationSpecificClientCertificateMaker,
)
from ...security_alert import SecurityAlert

##############################################################################
type LastInputSetter = Callable[[InputContent | None], None]
"""Type of a setter for the last input."""
type LastInputGetter = Callable[[], InputContent | None]
"""Type of a getter for the last input."""


##############################################################################
async def document(uri: AnyURI, request: OpenLocation, response: Response) -> Document:
    """Create a Document from a response.

    Args:
        uri: The URI of the document.
        request: The request that was made.
        response: The response that was received.

    Returns:
        A Document object.
    """
    return Document(
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


##############################################################################
async def handle_client_certificate_request(
    location: AnyURI, request_reason: str, client: Client, owner: Widget
) -> None:
    """Handle a request for a client certificate from a Gemini/Titan request.

    Args:
        location: The location making the request.
        request_reason: The reason for the client certificate request.
        client: The client to use for the request.
        owner: The widget that owns the request.
    """

    decision: ClientCertificatePickerResult = None

    # Check if there are any certificates available to use.
    if available_certificates := await client.client_cert_store.list_certificates():
        decision = await owner.app.push_screen_wait(
            ClientCertificatePicker(location, available_certificates)
        )

    # Bail if the user backed out.
    if decision is None:
        owner.notify("Client certificate request cancelled.", severity="warning")
        return

    # If the user selected an existing certificate, associate it with the location.
    if isinstance(decision, ClientCertificate):
        try:
            await client.client_cert_store.associate_scope(
                decision, location.with_path(None).with_query(None)
            )
        except (ValueError, RuntimeError) as error:
            owner.notify(
                f"Unable to associate client certificate for {location}:\n\n{error}",
                severity="error",
                title="Client Certificate Error",
            )
            return
    else:
        # The user elected to create a new certificate, so show the
        # certificate creation dialog.
        certificate_data: CertificateData | None = None
        if (
            certificate_data := await owner.app.push_screen_wait(
                LocationSpecificClientCertificateMaker(location, request_reason)
            )
        ) is None:
            owner.notify("Client certificate creation cancelled.", severity="warning")
            return

        # If they didn't bail on entering the new details, create the certificate.
        if certificate_data is not None:
            try:
                await client.client_cert_store.create_certificate(**certificate_data)
            except (ValueError, OSError, RuntimeError) as error:
                owner.notify(
                    f"Unable to create client certificate for {location}:\n\n{error}",
                    severity="error",
                    title="Client Certificate Error",
                )
                return

    # Finally, at this point, we've made *some* sort of change to the
    # certificate data so flag that up, and then re-request the original
    # location.
    owner.post_message(ClientCertificatesModified())
    owner.post_message(OpenLocation(location, allow_cached=False))


##############################################################################
async def handle_security_error(
    client: Client, error: SecurityError, uri: AnyURI, owner: Widget
) -> None:
    """Handle a security error from a Gemini/Titan request.

    Args:
        client: The client that contains the trust store.
        error: The security error to handle.
        uri: The URI that caused the security error.
        owner: The widget that owns the request.
    """
    if await owner.app.push_screen_wait(SecurityAlert(uri, str(error))):
        assert client.trust_store is not None
        await client.trust_store.forget(uri.host, uri.port)
        owner.post_message(OpenLocation(uri, allow_cached=False))
        owner.notify(
            f"Reset the trust status for {uri.host}:{uri.port}",
            title="Security Alert",
            severity="warning",
        )


### _glv.py ends here
