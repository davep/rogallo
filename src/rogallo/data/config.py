"""Code relating to the application's configuration file."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, fields
from functools import cache
from json import dumps, loads
from pathlib import Path
from typing import Final

##############################################################################
# Local imports.
from .locations import config_dir


##############################################################################
@dataclass
class Configuration:
    """The configuration data for the application."""

    theme: str | None = None
    """The theme for the application."""

    bindings: dict[str, str] = field(default_factory=dict)
    """Command keyboard binding overrides."""

    command_line_on_top: bool = False
    """Should the command line live at the top of the screen?"""

    displayable_content_types: list[str] = field(
        default_factory=lambda: [
            "text/gemini",
            "text/plain",
        ]
    )
    """The content types that can be displayed in the viewer."""

    handle_ansi_escape_sequences: bool = True
    """Should ANSI escape sequences be handled in text content?"""

    strip_emoji: bool = False
    """Should emoji be stripped from text content?"""

    history_visible: bool = False
    """Should the history panel be visible by default?"""

    bookmarks_visble: bool = False
    """Should the bookmarks panel be visible by default?"""

    show_link_tooltips: bool = True
    """Should tooltips be shown for links?"""

    show_preformat_tooltips: bool = True
    """Should tooltips be shown for preformatted text?"""

    disable_animations: bool = False
    """Should animations be disabled?"""

    home_page: str = "gemini://geminiprotocol.net/"
    """The home page for the application."""

    with_cache: bool = True
    """Should the application use a cache for remote content?"""

    cache_ttl: int = 3_600
    """The time-to-live for cached content, in seconds."""

    connection_timeout: int = 10
    """The connection timeout for network requests, in seconds."""

    read_timeout: int = 30
    """The read timeout for network requests, in seconds."""

    maximum_redirects: int = 5
    """The maximum number of redirects to follow for network requests."""

    stripe_links: bool = False
    """Should links be given alternating backgrounds to help them stand out?"""

    with_link_jumps: bool = True
    """Should the application support jumping to links via numeric labels?"""

    maximum_document_width: int = 0
    """The maximum width of a document, in characters. A value of 0 means no limit."""

    jump_progress_timeout: float = 1.0
    """The time in seconds before the jump progress resets."""


##############################################################################
def configuration_file() -> Path:
    """The path to the file that holds the application configuration.

    Returns:
        The path to the configuration file.
    """
    return config_dir() / "configuration.json"


##############################################################################
def save_configuration(configuration: Configuration) -> Configuration:
    """Save the given configuration.

    Args:
        The configuration to store.

    Returns:
        The configuration.
    """
    load_configuration.cache_clear()
    configuration_file().write_text(
        dumps(asdict(configuration), indent=4), encoding="utf-8"
    )
    return load_configuration()


##############################################################################
_WANTED: Final[set[str]] = {field.name for field in fields(Configuration)}
"""The set of fields that are wanted from the configuration file."""


##############################################################################
@cache
def load_configuration() -> Configuration:
    """Load the configuration.

    Returns:
        The configuration.

    Note:
        As a side-effect, if the configuration doesn't exist a default one
        will be saved to storage.

        This function is designed so that it's safe and low-cost to
        repeatedly call it. The configuration is cached and will only be
        loaded from storage when necessary.
    """
    source = configuration_file()
    return (
        Configuration(
            **{
                field: value
                for field, value in loads(source.read_text(encoding="utf-8")).items()
                if field in _WANTED
            }
        )
        if source.exists()
        else save_configuration(Configuration())
    )


##############################################################################
@contextmanager
def update_configuration() -> Iterator[Configuration]:
    """Context manager for updating the configuration.

    Loads the configuration and makes it available, then ensures it is
    saved.

    Example:
        ```python
        with update_configuration() as config:
            config.meaning = 42
        ```
    """
    configuration = load_configuration()
    try:
        yield configuration
    finally:
        save_configuration(configuration)


### config.py ends here
