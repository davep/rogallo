"""Provides code for handling a Titan request."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import Client, TitanURI

##############################################################################
# Local imports.
from ....messages import OpenLocation
from ...user_upload import UserUpload


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

    if upload := await owner.app.push_screen_wait(UserUpload(uri)):
        owner.notify(f"TODO: Perform the upload {upload!r}")


### titan.py ends here
