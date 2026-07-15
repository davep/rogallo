"""Provides code for saving and loading a list of trusted MIME types."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir

##############################################################################
type TrustedMIMETypes = set[str]
"""Type of a list of trusted MIME types."""


##############################################################################
def trusted_mime_types_file() -> Path:
    """Get the path for the trusted MIME types file.

    Returns:
        The path for the trusted MIME types file.
    """
    return data_dir() / "trusted_mime_types"


##############################################################################
def save_trusted_mime_types(mime_types: TrustedMIMETypes) -> None:
    """Save the trusted MIME types to storage.

    Args:
        mime_types: The trusted MIME types to save.
    """
    trusted_mime_types_file().write_text(
        "\n".join(sorted(mime_types)),
        encoding="utf-8",
    )


##############################################################################
def load_trusted_mime_types() -> TrustedMIMETypes:
    """Load the trusted MIME types from storage.

    Returns:
        The loaded trusted MIME types.
    """
    return (
        set(
            line.strip()
            for line in trusted_mime_types.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        if (trusted_mime_types := trusted_mime_types_file()).exists()
        else set()
    )


### trusted_mime_types.py ends here
