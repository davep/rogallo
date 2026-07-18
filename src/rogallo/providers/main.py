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
    AddLocationToBookmarks,
    Backward,
    ChangeCommandLineLocation,
    ClearCache,
    CopyDocumentToClipboard,
    CopyLocationToClipboard,
    Forward,
    GoHome,
    GoToParent,
    GoToRoot,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    Reload,
    SearchBookmarks,
    SearchHistory,
    SetHome,
    SetHomeToCurrentLocation,
    StripeLinks,
    ToggleBookmarks,
    ToggleHistory,
    ToggleLinkNumbers,
    ToggleView,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield from self.maybe(AddLocationToBookmarks)
        yield from self.maybe(Backward)
        yield ChangeCommandLineLocation()
        yield ChangeTheme()
        yield ClearCache()
        yield from self.maybe(CopyDocumentToClipboard)
        yield from self.maybe(CopyLocationToClipboard)
        yield from self.maybe(Forward)
        yield from self.maybe(GoHome)
        yield from self.maybe(GoToParent)
        yield from self.maybe(GoToRoot)
        yield Help()
        yield from self.maybe(JumpToCommandLine)
        yield from self.maybe(JumpToDocument)
        yield JumpToSidebar()
        yield Quit()
        yield from self.maybe(Reload)
        yield from self.maybe(SearchBookmarks)
        yield from self.maybe(SearchHistory)
        yield SetHome()
        yield from self.maybe(SetHomeToCurrentLocation)
        yield StripeLinks()
        yield from self.maybe(ToggleBookmarks)
        yield from self.maybe(ToggleHistory)
        yield ToggleLinkNumbers()
        yield from self.maybe(ToggleView)


### main.py ends here
