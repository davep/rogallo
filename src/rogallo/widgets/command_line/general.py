"""Provides general application commands for the command line."""

##############################################################################
# Python imports.
from collections.abc import Callable

##############################################################################
# Textual imports.
from textual.message import Message
from textual.widget import Widget

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import ChangeTheme, Help, Quit

##############################################################################
# Local imports.
from .base_command import InputCommand


##############################################################################
class GeneralCommand(InputCommand):
    """Base class for general commands."""

    MESSAGE: Callable[[], Message]
    """The message to send for the command."""

    @classmethod
    def handle(cls, text: str, for_widget: Widget) -> bool:
        """Handle the command.

        Args:
            text: The text of the command.
            for_widget: The widget to handle the command for.

        Returns:
            `True` if the command was handled; `False` if not.
        """
        if cls.is_command(text):
            if (message := getattr(cls, "MESSAGE", None)) is not None:
                for_widget.post_message(message())
            return True
        return False


##############################################################################
class HelpCommand(GeneralCommand):
    """Show the help screen"""

    COMMAND = "`!help`"
    ALIASES = "`?`"
    MESSAGE = Help


##############################################################################
class QuitCommand(GeneralCommand):
    """Quit the application"""

    COMMAND = "`!quit`"
    ALIASES = "`!q`"
    MESSAGE = Quit


##############################################################################
class ChangeThemeCommand(GeneralCommand):
    """Change the application theme"""

    COMMAND = "`!theme`"
    MESSAGE = ChangeTheme


### general.py ends here
