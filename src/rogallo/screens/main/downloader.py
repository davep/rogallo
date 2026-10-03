"""Provides a downloader for the rogallo application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Textual FSPicker imports.
from textual_fspicker import FileSave

##############################################################################
# Local imports.
from ...clients import Clients
from .uri_resolver import class_from_uri


##############################################################################
async def download(uri: str, clients: Clients, owner: Widget) -> None:
    """Download a URI using the appropriate client.

    Args:
        uri: The URI to download.
        clients: The clients to use for downloading.
    """

    # Turn the URI into a URI class so we know what we're working with.
    if (uri_class := class_from_uri(uri)) is None:
        owner.notify(f"Unable to download {uri}: unsupported scheme", severity="error")
        return
    location = uri_class(uri)

    # Prompt the user for the download location.
    if not (
        target_file := await owner.app.push_screen_wait(
            FileSave(
                title=f"Download {location}", default_file=Path(location.path).name
            )
        )
    ):
        owner.notify("Download cancelled.")
        return

    owner.notify(f"TODO: Downloading {location} to {target_file}")


### downloader.py ends here
