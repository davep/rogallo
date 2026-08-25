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
    AboutThisPage,
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
    HandOffToOperatingSystem,
    JumpToCommandLine,
    JumpToDocument,
    JumpToSidebar,
    OpenFile,
    PipeDocument,
    Reload,
    SaveSource,
    SearchBookmarks,
    SearchHistory,
    SetHome,
    SetHomeToCurrentLocation,
    StripeLinks,
    ToggleANSIEscapeSequenceHandling,
    ToggleCosyLinkNumbers,
    ToggleEmojiRemoval,
    ToggleLinkNumbers,
    ToggleSidebar,
    ToggleView,
    ViewChangeLog,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield from self.maybe(AboutThisPage)
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
        yield from self.maybe(HandOffToOperatingSystem)
        yield Help()
        yield from self.maybe(JumpToCommandLine)
        yield from self.maybe(JumpToDocument)
        yield JumpToSidebar()
        yield OpenFile()
        yield from self.maybe(PipeDocument)
        yield Quit()
        yield from self.maybe(Reload)
        yield from self.maybe(SaveSource)
        yield from self.maybe(SearchBookmarks)
        yield from self.maybe(SearchHistory)
        yield SetHome()
        yield from self.maybe(SetHomeToCurrentLocation)
        yield StripeLinks()
        yield ToggleANSIEscapeSequenceHandling()
        yield ToggleCosyLinkNumbers()
        yield ToggleEmojiRemoval()
        yield ToggleLinkNumbers()
        yield ToggleSidebar()
        yield from self.maybe(ToggleView)
        yield ViewChangeLog()


### main.py ends here
