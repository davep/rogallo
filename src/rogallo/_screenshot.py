"""Utility function for taking an ANSI screenshot."""

##############################################################################
# Python imports.
from collections.abc import Iterator
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app import App


##############################################################################
def _ansi_representation_of(app: App) -> Iterator[str]:
    """Get the ANSI representation of the Textual app's screen.

    Args:
        app: The Textual app to get the ANSI representation of.

    Returns:
        An iterator of strings representing the ANSI representation of the
        app's screen.
    """
    for strip in app.screen._compositor.render_strips():
        yield "".join(
            segment.style.render(
                segment.text,
                color_system=app.console._color_system,
            )
            if segment.style
            else segment.text
            for segment in strip
        )


##############################################################################
def save_ansi_screenshot(app: App, screenshot: Path | str) -> None:
    """Save the ANSI representation of the Textual app's screen to a file.

    Args:
        app: The Textual app to save the ANSI representation of.
        screenshot: The file path where the ANSI text output will be written.
    """
    Path(screenshot).expanduser().write_text(
        "\n".join(_ansi_representation_of(app)) + "\n", encoding="utf-8"
    )


### _screenshot.py ends here
