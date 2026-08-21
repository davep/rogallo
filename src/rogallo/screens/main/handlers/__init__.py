"""Provides the handlers for the various protocols."""

##############################################################################
# Local imports.
from .filesystem import handle_filesystem_request
from .finger import handle_finger_request
from .gemini import LastInputGetter, LastInputSetter, handle_gemini_request
from .gopher import handle_gopher_request
from .nex import handle_nex_request
from .spartan import handle_spartan_request

##############################################################################
# Exports.
__all__ = [
    "handle_filesystem_request",
    "handle_finger_request",
    "handle_gemini_request",
    "handle_gopher_request",
    "handle_nex_request",
    "handle_spartan_request",
    "LastInputGetter",
    "LastInputSetter",
]

### __init__.py ends here
