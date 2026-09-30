"""Code for loading up and migrating Rogallo's pre-v3 configuration."""

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass, field, fields, replace
from json import dumps, loads
from pathlib import Path
from typing import Final, Literal

##############################################################################
# Local imports.
from ..locations import config_dir
from ._io import save_configuration, save_configuration_from


##############################################################################
@dataclass
class LegacyConfiguration:
    """The pre-v3 legacy configuration."""

    migrated: bool = False
    theme: str | None = None
    bindings: dict[str, str] = field(default_factory=dict)
    command_line_on_top: bool = False
    displayable_content_types: list[str] = field(default_factory=list)
    handle_ansi_escape_sequences: bool = True
    strip_emoji: bool = False
    side_panel_visible: bool = False
    side_panel_on_right: bool = False
    side_panel_chosen_tab: str = "bookmarks"
    show_link_tooltips: bool = True
    show_preformat_tooltips: bool = True
    disable_animations: bool = False
    home_page: str = "gemini://geminiprotocol.net/"
    with_cache: bool = True
    cache_ttl: int = 3_600
    capsule_certificate_verify_mode: Literal["ca", "tofu", "hybrid", "off"] = "hybrid"
    connection_timeout: int = 10
    read_timeout: int = 30
    maximum_redirects: int = 5
    stripe_links: bool = False
    with_link_jumps: bool = True
    cosy_link_jumps: bool = False
    maximum_document_width: int = 0
    jump_progress_timeout: float = 1.0
    geminispace_link_icon: str = "⪢"
    fingerspace_link_icon: str = "☛"
    gopherspace_link_icon: str = "○"
    spartanspace_link_icon: str = "⪧"
    nexspace_link_icon: str = "☽"
    titanspace_link_icon: str = "⩓"
    otherspace_link_icon: str = "↗"
    list_item_bullet_icon: str = "•"
    client_certificate_used_icon: str = "⚿"
    verified_ca_icon: str = "⛉"
    verified_tofu_icon: str = "✓"
    verified_off_icon: str = "✗"
    unverified_icon: str = "•"
    external_editor: str | None = None
    blend_pre_formatted_with_background: list[str] = field(default_factory=lambda: [""])
    hide_preformatted: list[tuple[str, str]] = field(default_factory=list)
    gopher_show_type_badges: bool = True
    gopher_type_badges: dict[str, str] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
    guess_language_for_syntax_highlighting_text_documents: bool = True
    convert_markdown_to_gemtext: bool = True
    toolbar_visible: bool = True
    toolbar_contents: list[str | list[str]] = field(default_factory=list)
    toolbar_can_get_focus: bool = False
    toolbar_tooltips: bool = True
    footer_visible: bool = True
    command_line_prompt: str = ">"
    busy_indicator_cells: str = ""


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

    if legacy_config.gopher_type_badges:
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

    if legacy_config.hide_preformatted:
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

    if legacy_config.toolbar_contents:
        from .toolbar import ToolbarConfiguration

        save_configuration_from(
            "toolbar",
            ToolbarConfiguration(
                buttons=[
                    {"command": button, "label": None}
                    if isinstance(button, str)
                    else {"command": button[0], "label": button[1]}
                    for button in legacy_config.toolbar_contents
                ],
                can_get_focus=legacy_config.toolbar_can_get_focus,
                show_tooltips=legacy_config.toolbar_tooltips,
                visible=legacy_config.toolbar_visible,
            ),
        )

    save_legacy_configuration(replace(legacy_config, migrated=True))

    # TODO:
    # - Theme
    # - Displayable content types
    # - Handle ANSI escape sequences
    # - Strip emoji
    # - Side panel visible
    # - Side panel on right
    # - Side panel chosen tab
    # - Stripe links
    # - With link jumps
    # - Cosy link jumps
    # - Anything else I've forgotten.


### legacy.py ends here
