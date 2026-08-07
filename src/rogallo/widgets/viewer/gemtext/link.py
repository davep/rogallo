"""Provides a widget for displaying a Gemtext link."""

##############################################################################
# Python imports.
from pathlib import Path
from urllib.parse import urlparse

##############################################################################
# Gemtext imports.
from gemtext import Line, Link

##############################################################################
# Port70 imports.
from port70 import GopherURI

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup
from textual.events import Click
from textual.getters import query_one
from textual.reactive import var
from textual.widgets import Label

##############################################################################
# Textual enhanced imports.
from textual_enhanced.binding import HelpfulBinding

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ....data import load_configuration
from ....messages import OpenLocation, OpenURI
from ....preflight import (
    is_finger_uri,
    is_gopher_uri,
    is_likely_capsule,
    is_spartan_uri,
)
from ....types import RogalloLocation, SpartanURINeedingData
from .content_filter import GemtextContent
from .icons import icon


##############################################################################
class GemtextLink(Horizontal, can_focus=True):
    """A widget for displaying a Gemtext link."""

    DEFAULT_CSS = """
    GemtextLink {
        margin: 0 2 0 0;
        height: auto;
        pointer: pointer;

        #icon {
            color: $text-primary;
            margin-right: 1;
            height: auto;
        }

        &.--visited #icon {
            color: $text-primary 50%;
        }

        #text-wrap {
            height: auto;
        }

        #text {
            margin-right: 2;
        }

        #jump {
            display: none;
            color: $text-muted 30%;
            height: 100%;
        }

        &:hover {
            background: $block-hover-background !important;
        }

        &:focus {
            #text-wrap, #jump {
                color: $block-cursor-foreground;
                background: $block-cursor-background;
            }
            #jump {
                color: $text;
                text-style: bold;
            }
        }
    }
    """

    HELP = """
    ## Link

    This is a link to either another document, or an external resource that
    will be handled by your system.
    """

    BINDINGS = [HelpfulBinding("enter", "open_link", "Open link", show=False)]

    visited: var[bool] = var(False, toggle_class="--visited")
    """Whether the link has been visited or not."""
    jump_number: var[int | None] = var(None)
    """The jump number for the link."""

    _normalised_uri: var[str] = var("")
    """The normalised URI to use when opening the link."""

    _jump_link = query_one("#jump", Label)
    """The jump link label."""
    _icon = query_one("#icon", Label)
    """The icon label."""

    def __init__(self, link: Line) -> None:
        """Initialize a Gemtext link widget.

        Args:
            line: The Gemtext link to display.
        """
        super().__init__()
        assert isinstance(link, Link)
        self._link = link
        """The link data."""
        self._normalised_uri = link.uri
        """The normalised URI to use when opening the link."""

    @property
    def normalised_uri(self) -> str:
        """The normalised URI to use when opening the link."""
        return self._normalised_uri

    def _best_icon(self) -> str:
        """Get the best icon for the link based on its URI."""
        for checker, icon_name in (
            (is_likely_capsule, "geminispace_link_icon"),
            (is_finger_uri, "fingerspace_link_icon"),
            (is_gopher_uri, "gopherspace_link_icon"),
            (is_spartan_uri, "spartanspace_link_icon"),
        ):
            if checker(self.normalised_uri):
                return icon(icon_name)
        return icon("otherspace_link_icon")

    def normalise_uri(self, base_uri: RogalloLocation | None) -> None:
        """Normalise the URI of the link against a base URI.

        Args:
            base_uri: The base URI to normalise against.
        """
        if base_uri is None:
            return
        if urlparse(self._normalised_uri).scheme:
            return
        if isinstance(base_uri, (GeminiURI, GopherURI, SpartanURI)):
            self._normalised_uri = str(base_uri.resolve(self._link.uri))
        elif isinstance(base_uri, Path):
            self._normalised_uri = (base_uri.parent / self._link.uri).resolve().as_uri()
        if self.is_mounted:
            self._icon.update(self._best_icon())

    def _watch__normalised_uri(self) -> None:
        """Watch for changes to the normalised URI."""
        if load_configuration().show_link_tooltips:
            self.tooltip = self._normalised_uri

    def _watch_jump_number(self) -> None:
        """Watch for changes to the jump number."""
        self._jump_link.update(
            "" if self.jump_number is None else f"[{self.jump_number}]"
        )
        self.set_class(
            self.jump_number is not None and not bool(self.jump_number % 2),
            "--stripe",
        )

    def compose(self) -> ComposeResult:
        """Compose the Gemtext link widget."""
        yield Label(self._best_icon(), id="icon")
        with HorizontalGroup():
            with HorizontalGroup(id="text-wrap"):
                yield Label(
                    GemtextContent.filter(self._link),
                    id="text",
                    markup=False,
                    shrink=True,
                )
            yield Label(id="jump", markup=False)

    def _navigate_to_uri(self) -> None:
        """Navigate to the normalised URI."""
        self.post_message(OpenURI(self._normalised_uri, allow_cached=False))

    @on(Click)
    def _action_open_link(self) -> None:
        """Open the link."""
        self._navigate_to_uri()


##############################################################################
class SpartanPromptLink(GemtextLink):
    """A widget for displaying a Gemtext link that is a Spartan prompt."""

    def _navigate_to_uri(self) -> None:
        """Navigate to the normalised URI."""
        self.post_message(
            OpenLocation(
                SpartanURINeedingData(self._normalised_uri),
                allow_cached=False,
                do_not_record_in_history=True,
            )
        )


### link.py ends here
