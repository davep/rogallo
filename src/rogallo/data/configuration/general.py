"""Code relating to the application's configuration file."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cache
from typing import Literal

##############################################################################
# Local imports.
from ._io import load_configuration_into, save_configuration_from


##############################################################################
@dataclass
class GeneralConfiguration:
    """The general configuration data for the application."""

    command_line_on_top: bool = False
    """Should the command line live at the top of the screen?"""

    show_link_tooltips: bool = True
    """Should tooltips be shown for links?"""

    disable_animations: bool = False
    """Should animations be disabled?"""

    with_cache: bool = True
    """Should the application use a cache for remote content?"""

    cache_ttl: int = 3_600
    """The time-to-live for cached content, in seconds."""

    capsule_certificate_verify_mode: Literal["ca", "tofu", "hybrid", "off"] = "hybrid"
    """The certificate verification mode Gemini capsules.

    One of: `ca`, `tofu`, `hybrid` or `off`.
    """

    connection_timeout: int = 10
    """The connection timeout for network requests, in seconds."""

    read_timeout: int = 30
    """The read timeout for network requests, in seconds."""

    maximum_redirects: int = 5
    """The maximum number of redirects to follow for network requests."""

    maximum_document_width: int = 0
    """The maximum width of a document, in characters. A value of 0 means no limit."""

    jump_progress_timeout: float = 1.0
    """The time in seconds before the jump progress resets."""

    external_editor: str | None = None
    """The external editor to use for editing text content."""

    guess_language_for_syntax_highlighting_text_documents: bool = True
    """Whether to guess the language for syntax highlighting of text documents."""

    convert_markdown_to_gemtext: bool = True
    """Whether to convert Markdown documents to Gemtext for display."""

    footer_visible: bool = True
    """Whether the footer is visible."""

    command_line_prompt: str = ">"
    """The prompt to use for the command line."""

    busy_indicator_cells: str = ""
    """The characters to use for the busy indicator."""


##############################################################################
def save_general(configuration: GeneralConfiguration) -> GeneralConfiguration:
    """Save the general configuration.

    Args:
        configuration: The configuration to store.

    Returns:
        The configuration.
    """
    load_general.cache_clear()
    save_configuration_from("general", configuration)
    return load_general()


##############################################################################
@cache
def load_general() -> GeneralConfiguration:
    """Load the general configuration.

    Returns:
        The general configuration.

    Note:
        This function is designed so that it's safe and low-cost to
        repeatedly call it. The configuration is cached and will only be
        loaded from storage when necessary.
    """
    return load_configuration_into(GeneralConfiguration, "general")


##############################################################################
@contextmanager
def update_general() -> Iterator[GeneralConfiguration]:
    """Context manager for updating the general configuration.

    Loads the general configuration and makes it available, then ensures it
    is saved.

    Example:
        ```python
        with update_general() as config:
            config.meaning = 42
        ```

    Yields:
        The general configuration.
    """
    configuration = load_general()
    try:
        yield configuration
    finally:
        save_general(configuration)


### config.py ends here
