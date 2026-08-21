"""Code for dealing with unsupported things."""

##############################################################################
# Python imports.
from pathlib import Path
from urllib.parse import urlparse
from webbrowser import open as open_in_browser

##############################################################################
# Port79 imports.
from port79 import FingerURI

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ...data import (
    load_trusted_mime_types,
    load_trusted_schemes,
    save_trusted_mime_types,
    save_trusted_schemes,
)
from ..confirm_unsupported import ConfirmUnsupportedURI
from .local_messages import OpenUnsupportedMIMEType, OpenUnsupportedURI


##############################################################################
async def maybe_open_unsupported_uri(
    message: OpenUnsupportedURI, owner: Widget
) -> None:
    """Maybe open an unsupported URI in the system's web browser.

    Args:
        message: The message containing the unsupported URI.
    """

    # Because we want to gatekeep which schemes get passed on, let's
    # grab the scheme.
    try:
        scheme = urlparse(message.uri).scheme.lower()
    except ValueError:
        return

    # If there's no scheme, let's GTFO.
    if not scheme:
        owner.notify(f"Unable to open {message.uri}: no scheme found", severity="error")
        return

    # If the scheme isn't trusted, let's see what the user wants to do about it.
    if not (open_uri := scheme in (trusted_schemes := load_trusted_schemes())):
        match await owner.app.push_screen_wait(
            ConfirmUnsupportedURI(
                message.uri,
                f"The scheme '{scheme}' is not supported by Rogallo. "
                "Do you want to open the URI in your external browser?",
            )
        ):
            case "once":
                open_uri = True
            case "always":
                open_uri = True
                trusted_schemes.add(scheme)
                save_trusted_schemes(trusted_schemes)

    # At this point, if the user has consented to opening the URI based
    # on the scheme, let's do it.
    if open_uri:
        open_in_browser(message.uri)


##############################################################################
async def maybe_open_unsupported_mime_type(
    message: OpenUnsupportedMIMEType, owner: Widget
) -> None:
    """Open an unsupported MIME typed location in the system's web browser.

    Args:
        message: The message containing the unsupported MIME type.
    """

    # There's no reason why we should be here for Finger URIs.
    if isinstance(message.location, FingerURI):
        owner.notify(
            f"Unexpected request to open {message.location}: please let Dave know",
            severity="warning",
        )
        return

    # If the MIME type isn't trusted, let's see what the user wants to
    # do about it.
    if not (
        open_uri := message.mime_type
        in (trusted_mime_types := load_trusted_mime_types())
    ):
        match await owner.app.push_screen_wait(
            ConfirmUnsupportedURI(
                str(message.location),
                f"The MIME type '{message.mime_type}' is not supported by Rogallo. "
                "Do you want to open the location in your external browser?",
            )
        ):
            case "once":
                open_uri = True
            case "always":
                open_uri = True
                trusted_mime_types.add(message.mime_type)
                save_trusted_mime_types(trusted_mime_types)

    # At this point, if the user has consented to opening the location
    # based on the MIME type, let's do it.
    if open_uri:
        open_in_browser(
            message.location.resolve().as_uri()
            if isinstance(message.location, Path)
            else str(message.location)
        )


### unsupported.py ends here
