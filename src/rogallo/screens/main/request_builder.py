"""Provides code that builds a URI requester."""

##############################################################################
# Python imports.
from collections.abc import Awaitable

##############################################################################
# Port70 imports.
from port70 import GopherURI

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Port1900 imports.
from port1900 import NexURI

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ...cache import ContentCache
from ...document import Document
from ...messages import OpenLocation
from .clients import Clients
from .handlers import (
    LastInputGetter,
    LastInputSetter,
    handle_finger_request,
    handle_gemini_request,
    handle_gopher_request,
    handle_nex_request,
    handle_spartan_request,
)


##############################################################################
def build_request(
    clients: Clients,
    message: OpenLocation,
    cache: ContentCache,
    owner: Widget,
    current_document: Document,
    set_last_input: LastInputSetter,
    get_last_input: LastInputGetter,
) -> Awaitable[None] | None:
    if isinstance(message.location, FingerURI):
        return handle_finger_request(
            request=message,
            client=clients.finger,
            owner=owner,
        )
    elif isinstance(message.location, GeminiURI):
        return handle_gemini_request(
            request=message,
            client=clients.gemini,
            owner=owner,
            cache=cache,
            set_last_input=set_last_input,
            get_last_input=get_last_input,
        )
    elif isinstance(message.location, GopherURI):
        return handle_gopher_request(
            request=message,
            client=clients.gopher,
            owner=owner,
            cache=cache,
            current_document=current_document,
        )
    elif isinstance(message.location, SpartanURI):
        return handle_spartan_request(
            request=message,
            client=clients.spartan,
            owner=owner,
            cache=cache,
        )
    elif isinstance(message.location, NexURI):
        return handle_nex_request(
            request=message,
            client=clients.nex,
            owner=owner,
            cache=cache,
        )
    return None


### request_builder.py ends here
