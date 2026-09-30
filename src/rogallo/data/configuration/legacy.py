"""Code for loading up and migrating Rogallo's pre-v3 configuration."""

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass, field, fields, replace
from json import dumps, loads
from pathlib import Path
from typing import Final, Literal

##############################################################################
# GopherMap imports.
from gophermap import ItemType

##############################################################################
# Local imports.
from ..locations import config_dir
from ._io import save_configuration, save_configuration_from


##############################################################################
@dataclass
class LegacyConfiguration:
    """The pre-v3 legacy configuration."""

    migrated: bool = False
    """Whether the configuration has been migrated to the new format."""

    theme: str | None = None
    """The theme for the application."""

    bindings: dict[str, str] = field(default_factory=dict)
    """Command keyboard binding overrides."""

    command_line_on_top: bool = False
    """Should the command line live at the top of the screen?"""

    displayable_content_types: list[str] = field(default_factory=list)
    """The content types that can be displayed in the viewer."""

    handle_ansi_escape_sequences: bool = True
    """Should ANSI escape sequences be handled in text content?"""

    strip_emoji: bool = False
    """Should emoji be stripped from text content?"""

    side_panel_visible: bool = False
    """Should the sidepanel be visible?"""

    side_panel_on_right: bool = False
    """Should the sidepanel be on the right?"""

    side_panel_chosen_tab: str = "bookmarks"
    """The tab that should be chosen in the sidepanel."""

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

    stripe_links: bool = False
    """Should links be given alternating backgrounds to help them stand out?"""

    with_link_jumps: bool = True
    """Should the application support jumping to links via numeric labels?"""

    cosy_link_jumps: bool = False
    """Should the numeric labels be displayed in a cosy way?"""

    maximum_document_width: int = 0
    """The maximum width of a document, in characters. A value of 0 means no limit."""

    jump_progress_timeout: float = 1.0
    """The time in seconds before the jump progress resets."""

    geminispace_link_icon: str = "⪢"
    """The icon to use for links to gemini:// URIs."""

    fingerspace_link_icon: str = "☛"
    """The icon to use for links to finger:// URIs."""

    gopherspace_link_icon: str = "○"
    """The icon to use for links to gopher:// URIs."""

    spartanspace_link_icon: str = "⪧"
    """The icon to use for links to spartan:// URIs."""

    nexspace_link_icon: str = "☽"
    """The icon to use for links to nex:// URIs."""

    titanspace_link_icon: str = "⩓"
    """The icon to use for links to titan:// URIs."""

    otherspace_link_icon: str = "↗"
    """The icon to use for non-gemini URIs."""

    list_item_bullet_icon: str = "•"
    """The icon to use for list item bullets."""

    client_certificate_used_icon: str = "⚿"
    """The icon to use for indicating that a client certificate was used."""

    verified_ca_icon: str = "⛉"
    """The icon to use for indicating that a server was verified by a CA."""

    verified_tofu_icon: str = "✓"
    """The icon to use for indicating that a server was verified by TOFU."""

    verified_off_icon: str = "✗"
    """The icon to use for indicating that server was off."""

    unverified_icon: str = "•"
    """The icon to use for indicating that a server was not verified."""

    external_editor: str | None = None
    """The external editor to use for editing text content."""

    blend_pre_formatted_with_background: list[str] = field(default_factory=lambda: [""])
    """List of types of pre-formatted text to blend with the background."""

    hide_preformatted: list[tuple[str, str]] = field(default_factory=list)
    """List of (URI-prefix, alt-text) tuples of pre-formatted text to hide."""

    gopher_show_type_badges: bool = True
    """Whether to show badges for Gopher item types."""

    gopher_type_badges: dict[str, str] = field(
        default_factory=lambda: {
            ItemType.TEXT.value: "📄",
            ItemType.MENU.value: "📁",
            ItemType.CSO.value: "📇",
            ItemType.ERROR.value: "❌",
            ItemType.BINHEX.value: "📦",
            ItemType.DOS_FILE.value: "💾",
            ItemType.UUENCODED.value: "📜",
            ItemType.INDEX_SEARCH.value: "🔍",
            ItemType.TELNET.value: "🖥️",
            ItemType.BINARY.value: "📦",
            ItemType.INFO.value: "ℹ️",
            ItemType.GIF.value: "🖼️",
            ItemType.IMAGE.value: "🖼️",
            ItemType.HTML.value: "🌐",
            ItemType.DOCUMENT.value: "📄",
            ItemType.AUDIO.value: "🎵",
            ItemType.PDF.value: "📄",
            ItemType.XML.value: "📄",
            ItemType.UNKNOWN.value: "❓",
        }
    )
    """The badges to use for Gopher item types."""

    aliases: dict[str, str] = field(
        default_factory=lambda: {
            "fg": "gopher://gopher.floodgap.com/1/v2/vs?{q}",
            "gp": "gemini://gemi.dev/cgi-bin/wp.cgi/search?{q}",
            "ken": "gemini://kennedy.gemi.dev/search?{q}",
            "tlgs": "gemini://tlgs.one/search?{q}",
        }
    )
    """Aliases to use in the command line."""

    guess_language_for_syntax_highlighting_text_documents: bool = True
    """Whether to guess the language for syntax highlighting of text documents."""

    convert_markdown_to_gemtext: bool = True
    """Whether to convert Markdown documents to Gemtext for display."""

    toolbar_visible: bool = True
    """Whether the toolbar is visible."""

    toolbar_contents: list[str | list[str]] = field(
        default_factory=lambda: [
            ["GoHome", "⌂"],
            ["Reload", "↻"],
            ["Backward", "◀◀"],
            ["Forward", "▶▶"],
            ["GoToParent", "↑"],
            ["GoToRoot", "⇈"],
            ["SearchHistory", "◷"],
            ["SearchBookmarks", "★"],
            ["ToggleView", "⇋"],
        ]
    )
    """The contents of the toolbar."""

    toolbar_can_get_focus: bool = False
    """Whether the toolbar can get focus."""

    toolbar_tooltips: bool = True
    """Whether the toolbar buttons have tooltips."""

    footer_visible: bool = True
    """Whether the footer is visible."""

    command_line_prompt: str = ">"
    """The prompt to use for the command line."""

    busy_indicator_cells: str = ""
    """The characters to use for the busy indicator."""


##############################################################################
def configuration_file() -> Path:
    """The path to the file that holds the application configuration.

    Returns:
        The path to the configuration file.
    """
    return config_dir() / "configuration.json"


##############################################################################
def save_legacy_configuration(configuration: LegacyConfiguration) -> None:
    """Save the given configuration.

    Args:
        The configuration to store.
    """
    configuration_file().write_text(
        dumps(asdict(configuration), indent=4), encoding="utf-8"
    )


##############################################################################
_WANTED: Final[set[str]] = {field.name for field in fields(LegacyConfiguration)}
"""The set of fields that are wanted from the configuration file."""


##############################################################################
def load_legacy_configuration() -> LegacyConfiguration | None:
    """Load the configuration.

    Returns:
        The configuration, or None if it doesn't exist.
    """
    if not (source := configuration_file()).is_file():
        return None
    return LegacyConfiguration(
        **{
            field: value
            for field, value in loads(source.read_text(encoding="utf-8")).items()
            if field in _WANTED
        }
    )


##############################################################################
def migrate_legacy_configuration() -> None:
    """Migrate the legacy configuration to the new format."""
    if (legacy_config := load_legacy_configuration()) is None:
        return
    if legacy_config.migrated:
        return
    print("Migrating legacy configuration to new format...")

    from .general import GeneralConfiguration, save_general

    save_general(
        GeneralConfiguration(
            command_line_on_top=legacy_config.command_line_on_top,
            show_link_tooltips=legacy_config.show_link_tooltips,
            disable_animations=legacy_config.disable_animations,
            with_cache=legacy_config.with_cache,
            cache_ttl=legacy_config.cache_ttl,
            capsule_certificate_verify_mode=legacy_config.capsule_certificate_verify_mode,
            connection_timeout=legacy_config.connection_timeout,
            read_timeout=legacy_config.read_timeout,
            maximum_redirects=legacy_config.maximum_redirects,
            maximum_document_width=legacy_config.maximum_document_width,
            jump_progress_timeout=legacy_config.jump_progress_timeout,
            external_editor=legacy_config.external_editor,
            guess_language_for_syntax_highlighting_text_documents=legacy_config.guess_language_for_syntax_highlighting_text_documents,
            convert_markdown_to_gemtext=legacy_config.convert_markdown_to_gemtext,
            footer_visible=legacy_config.footer_visible,
            command_line_prompt=legacy_config.command_line_prompt,
            busy_indicator_cells=legacy_config.busy_indicator_cells,
        )
    )

    save_configuration("aliases", legacy_config.aliases)

    if legacy_config.bindings:
        save_configuration("bindings", legacy_config.bindings)

    from .gopher import GopherConfiguration

    save_configuration_from(
        "gopher",
        GopherConfiguration(
            show_type_badges=legacy_config.gopher_show_type_badges,
            type_badges=legacy_config.gopher_type_badges,
        ),
    )

    save_configuration(
        "icons",
        {
            "geminispace_link": legacy_config.geminispace_link_icon,
            "fingerspace_link": legacy_config.fingerspace_link_icon,
            "gopherspace_link": legacy_config.gopherspace_link_icon,
            "spartanspace_link": legacy_config.spartanspace_link_icon,
            "nexspace_link": legacy_config.nexspace_link_icon,
            "titanspace_link": legacy_config.titanspace_link_icon,
            "otherspace_link": legacy_config.otherspace_link_icon,
            "list_item_bullet": legacy_config.list_item_bullet_icon,
            "client_certificate_used": legacy_config.client_certificate_used_icon,
            "verified_ca": legacy_config.verified_ca_icon,
            "verified_tofu": legacy_config.verified_tofu_icon,
            "verified_off": legacy_config.verified_off_icon,
            "unverified": legacy_config.unverified_icon,
        },
    )

    from .preformatted import PreformattedConfiguration

    save_configuration_from(
        "preformatted",
        PreformattedConfiguration(
            blend_with_background=legacy_config.blend_pre_formatted_with_background,
            hide=[
                {"uri_prefix": uri, "alt_text": alt_text}
                for uri, alt_text in legacy_config.hide_preformatted
            ],
            tooltips=legacy_config.show_preformat_tooltips,
        ),
    )

    # preformatted
    # toolbar

    save_legacy_configuration(replace(legacy_config, migrated=True))


### legacy.py ends here
