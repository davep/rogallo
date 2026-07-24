"""Provides a modal screen for getting user input."""

##############################################################################
# Python imports.
from os import getenv
from pathlib import Path
from subprocess import run
from tempfile import NamedTemporaryFile

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.content import Content
from textual.getters import query_one
from textual.screen import ModalScreen
from textual.widgets import TextArea

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ..types import DEFAULT_GEMINI_EXTENSION


##############################################################################
class UserInput(ModalScreen[str | None]):
    """A modal screen to get input from the user."""

    CSS = """
    UserInput {
        align: center middle;

        TextArea, TextArea:focus {
            border: round $border;
            width: 60%;
            padding: 1;
            height: auto;
            max-height: 60%;

            &.--too-long {
                border: round $text-error;
                background: $error;
            }
        }

        &.--sensitive TextArea {
            color: $text 10%;
        }
    }
    """

    BINDINGS = [
        ("escape", "escape"),
        ("f2", "submit"),
        ("f3", "edit_externally"),
    ]

    _input = query_one(TextArea)
    """The input text area."""

    def __init__(
        self, location: GeminiURI, prompt: str, sensitive: bool, default: str = ""
    ) -> None:
        """Initialise the object.

        Args:
            request_from: The request that prompted this input.
            prompt: The prompt to display to the user.
            sensitive: Whether the input is sensitive.
            default: The default value to display in the input area.
        """
        super().__init__(classes=("--sensitive" if sensitive else ""))
        self._location = location
        """The location making the request."""
        self._prompt = prompt.strip()
        """The prompt to display to the user."""
        self._sensitive = sensitive
        """Whether the input is sensitive."""
        self._default = default
        """The default value to display in the input area."""

    def compose(self) -> ComposeResult:
        """Compose the input dialog."""
        yield (
            user_input := TextArea(
                self._default,
                highlight_cursor_line=False,
                placeholder="Enter your input here...",
            )
        )
        user_input.border_title = Content(
            self._prompt
            or (
                f"{'Sensitive input' if self._sensitive else 'Input'} for {self._location}"
                if self._location
                else "Input"
            )
        )

    @property
    def _current_text(self) -> str:
        """The current text in the input area."""
        return self._input.text

    @property
    def _current_query(self) -> GeminiURI:
        """The current query in the input area."""
        return self._location.with_query(self._current_text)

    @property
    def _external_editor(self) -> str | None:
        """The external editor to use, if any."""
        return getenv("VISUAL") or getenv("EDITOR") or None

    def _update_subtitle(self) -> None:
        """Update the subtitle of the input area."""
        footer = "F2: Submit"
        if bool(self._external_editor):
            footer += " | F3: $EDITOR"
        if not self._input.text:
            self._input.border_subtitle = footer
        elif self._current_query.is_too_long:
            self._input.border_subtitle = "Input is too long!"
        else:
            self._input.border_subtitle = f"{footer} ({self._current_query.bytes_left})"

    @on(TextArea.Changed)
    def _limit_check(self) -> None:
        """Check if the input is too long."""
        self._input.set_class(self._current_query.is_too_long, "--too-long")
        self._update_subtitle()

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is mounted."""
        self._update_subtitle()

    def action_submit(self) -> None:
        """Accept the input."""
        if not self._current_query.is_too_long:
            self.dismiss(self._current_text)

    def action_escape(self) -> None:
        """Escape out without getting the input."""
        self.dismiss(None)

    def action_edit_externally(self) -> None:
        """Edit the input in an external editor."""
        if not bool(editor := self._external_editor):
            return
        with NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8", suffix=DEFAULT_GEMINI_EXTENSION
        ) as temp_file:
            user_input = Path(temp_file.name)
            temp_file.write(self._current_text)
            temp_file.close()
            try:
                with self.app.suspend():
                    run((editor, user_input))
                self._input.text = user_input.read_text(encoding="utf-8")
            finally:
                user_input.unlink(missing_ok=True)


### user_input.py ends here
