"""Provide code for downloading and saving content."""

##############################################################################
# Textual imports.
from textual.widget import Widget

##############################################################################
# Local imports.
from ....messages import DownloadLocation


##############################################################################
def save_download(request: DownloadLocation, content: bytes, owner: Widget) -> None:
    """Save the downloaded content to the target file.

    Args:
        request: The download request containing the target file.
        content: The content to save.
    """
    try:
        request.target.write_bytes(content)
    except OSError as error:
        owner.notify(
            f"Failed to save downloaded content to {request.target}:\n\n{error}",
            severity="error",
            title="Download Error",
        )
        return
    owner.notify(
        f"Downloaded {request.location} to {request.target}", title="Download Complete"
    )


### _download.py ends here
