"""Provides code for loading and saving trusted sets."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir

##############################################################################
type TrustedSet = set[str]
"""Type of a trusted set."""


##############################################################################
def _save_set(trusted_type: str, trusted_set: TrustedSet) -> None:
    """Save the trusted set to storage.

    Args:
        trusted_type: The type of the trusted set.
        trusted_set: The trusted set to save.
    """
    (data_dir() / trusted_type).write_text(
        "\n".join(sorted(trusted_set)), encoding="utf-8"
    )


##############################################################################
def _load_set(trusted_type: str) -> TrustedSet:
    """Load a trusted set from storage.

    Args:
        trusted_type: The type of the trusted set.

    Returns:
        The loaded trusted set.
    """
    return (
        set(
            line.strip()
            for line in trusted_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        if (trusted_file := (data_dir() / trusted_type)).exists()
        else set()
    )


##############################################################################
def save_trusted_schemes(schemes: TrustedSet) -> None:
    """Save the trusted schemes to storage.

    Args:
        schemes: The trusted schemes to save.
    """
    _save_set("trusted_schemes", schemes)


##############################################################################
def load_trusted_schemes() -> TrustedSet:
    """Load the trusted schemes from storage.

    Returns:
        The loaded trusted schemes.
    """
    return _load_set("trusted_schemes")


##############################################################################
def save_trusted_mime_types(mime_types: TrustedSet) -> None:
    """Save the trusted MIME types to storage.

    Args:
        mime_types: The trusted MIME types to save.
    """
    _save_set("trusted_mime_types", mime_types)


##############################################################################
def load_trusted_mime_types() -> TrustedSet:
    """Load the trusted MIME types from storage.

    Returns:
        The loaded trusted MIME types.
    """
    return _load_set("trusted_mime_types")


##############################################################################
def known_hosts() -> Path:
    """The path to the known hosts file.

    Returns:
        The path to the known hosts file.
    """
    return data_dir() / "known_hosts"


### trusted_sets.py ends here
