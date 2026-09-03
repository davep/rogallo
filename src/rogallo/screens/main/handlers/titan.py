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

    owner.notify(f"TODO: Handling Titan request for {request.location}")


### titan.py ends here
