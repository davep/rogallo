"""Provides code for saving and loading a list of trusted schemes"""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir

##############################################################################
type TrustedSchemes = set[str]
"""Type of a list of trusted schemes."""


##############################################################################
def trusted_schemes_file() -> Path:
    """Get the path for the trusted schemes file.

    Returns:
        The path for the trusted schemes file.
    """
    return data_dir() / "trusted_schemes"


##############################################################################
def save_trusted_schemes(schemes: TrustedSchemes) -> None:
    """Save the trusted schemes to storage.

    Args:
        schemes: The trusted schemes to save.
    """
    trusted_schemes_file().write_text(
        "\n".join(sorted(schemes)),
        encoding="utf-8",
    )


##############################################################################
def load_trusted_schemes() -> TrustedSchemes:
    """Load the trusted schemes from storage.

    Returns:
        The loaded trusted schemes.
    """
    return (
        set(
            line.strip()
            for line in trusted_schemes.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        if (trusted_schemes := trusted_schemes_file()).exists()
        else set()
    )


### trusted_schemes.py ends here
