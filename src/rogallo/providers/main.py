"""Provides the main application commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import (
    ChangeTheme,
    CommandHits,
    CommandsProvider,
    Help,
    Quit,
)

##############################################################################
# Local imports.
from ..commands import (
    Backward,
    ChangeCommandLineLocation,
    Forward,
    JumpToCommandLine,
    JumpToDocument,
    Reload,
    ToggleHistory,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield ChangeCommandLineLocation()
        yield ChangeTheme()
        yield Help()
        yield Quit()
        yield from self.maybe(JumpToCommandLine)
        yield from self.maybe(JumpToDocument)
        yield from self.maybe(Backward)
        yield from self.maybe(Forward)
        yield from self.maybe(ToggleHistory)
        yield from self.maybe(Reload)


### main.py ends here
