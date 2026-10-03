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
# Wasat imports.
from wasat import GeminiURI, SecurityError, URIError

##############################################################################
# Local imports.
from ...clients import Clients
from .uri_resolver import class_from_uri


##############################################################################
async def _download_gemini(
    location: GeminiURI, target: Path, clients: Clients, owner: Widget
) -> None:
    """Download a Gemini URI to a target file.

    Args:
        location: The Gemini URI to download.
        target: The target file to download to.
        clients: The clients to use for downloading.
        owner: The widget that owns the request.
    """
    try:
        response = await clients.gemini.request(location)
    except (ConnectionError, SecurityError, URIError) as error:
        owner.notify(f"Unable to download {location}: {error}", severity="error")
        return

    if not response.status.is_success:
        owner.notify(
            f"Unable to download {location}: {response.status} {response.meta}",
            severity="error",
        )
        return

    # Write the content to the target file.
    try:
        target.write_bytes(await response.read())
    except OSError as error:
        owner.notify(f"Unable to write to {target}: {error}", severity="error")
        return

    owner.notify(f"Downloaded {location} to {target}")


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

    if isinstance(location, GeminiURI):
        await _download_gemini(location, target_file, clients, owner)
    else:
        owner.notify(
            f"Downloading for {location.scheme} URIs is not yet implemented",
            severity="warning",
        )


### downloader.py ends here
