"""Provides a modal screen for getting user input."""

##############################################################################
# Sybaritic imports.
from sybaritic import SpartanURI

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.content import Content
from textual.getters import query_one
from textual.screen import ModalScreen
from textual.widgets import Label, TextArea

##############################################################################
# Wasat imports.
from wasat import GeminiURI

##############################################################################
# Local imports.
from ..editor import edit_externally, external_editor


##############################################################################
class UserInput(ModalScreen[str | None]):
    """A modal screen to get input from the user."""

    CSS = """
    UserInput {
        align: center middle;

        &> VerticalGroup {
            background: $panel;
            border: round $border;
            width: 60%;
            padding: 1;
            height: auto;

            Label {
                color: $accent;
            }

            TextArea, TextArea:focus {
                background: transparent;
                border: none;
                border-top: solid $border;
                height: auto;
                max-height: 60vh;
                padding: 0;
            }

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

    _dialog = query_one(VerticalGroup)
    """The dialog container."""
    _input = query_one(TextArea)
    """The input text area."""

    def __init__(
        self,
        location: GeminiURI | SpartanURI,
        prompt: str,
        sensitive: bool = False,
        default: str = "",
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
        with VerticalGroup() as dialog:
            dialog.border_title = Content(
                f"{'Sensitive input' if self._sensitive else 'Input'} for {self._location}"
                if self._location
                else "Input"
            )
            yield Label(self._prompt, shrink=True, markup=False)
            yield TextArea(
                self._default,
                highlight_cursor_line=False,
                placeholder="Enter your input here...",
            )

    @property
    def _current_text(self) -> str:
        """The current text in the input area."""
        return self._input.text

    @property
    def _input_is_too_long(self) -> bool:
        """Whether the input is too long."""
        return (
            isinstance(self._location, GeminiURI)
            and self._location.with_query(self._current_text).is_too_long
        )

    def _update_subtitle(self) -> None:
        """Update the subtitle of the input area."""
        footer = "F2: Submit"
        if external_editor():
            footer += " | F3: $EDITOR"
        if not self._input.text:
            self._dialog.border_subtitle = footer
        elif self._input_is_too_long:
            self._dialog.border_subtitle = "Input is too long!"
        elif isinstance(self._location, GeminiURI):
            self._dialog.border_subtitle = f"{footer} ({self._location.with_query(self._current_text).bytes_left} left)"
        else:
            self._dialog.border_subtitle = f"{footer} ({len(self._current_text)} used)"

    @on(TextArea.Changed)
    def _limit_check(self) -> None:
        """Check if the input is too long."""
        self._dialog.set_class(self._input_is_too_long, "--too-long")
        self._update_subtitle()

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is mounted."""
        self._update_subtitle()

    def action_submit(self) -> None:
        """Accept the input."""
        if not self._input_is_too_long:
            self.dismiss(self._current_text)

    def action_escape(self) -> None:
        """Escape out without getting the input."""
        self.dismiss(None)

    def action_edit_externally(self) -> None:
        """Edit the input in an external editor."""
        self._input.text = edit_externally(self.app, self._input.text)


### user_input.py ends here
