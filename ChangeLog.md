# Rogallo ChangeLog

## v1.0.0

**Released: 2026-07-21**

- Prioritise showing locations from history rather than navigation history
  when doing a history search.
  ([#198](https://github.com/davep/rogallo/pull/198))

## v0.12.0

**Released: 2026-07-20**

- Added `!theme` as a command line command.
  ([#186](https://github.com/davep/rogallo/pull/186))
- Added an `OpenFile` command, which opens a file picker dialog for picking
  a local file to view. ([#188](https://github.com/davep/rogallo/pull/188))
- Entering the name of an existing directory in the command line now opens
  that directory in the file picker dialog.
  ([#188](https://github.com/davep/rogallo/pull/188))
- Added a `ToggleCosyLinkNumbers` command, which moves the link jump numbers
  over to the left of the link text or back to the right.
  ([#193](https://github.com/davep/rogallo/pull/193))
- Modified `ToggleEmojiRemoval` so that it *doesn't* remove emojis from
  pre-formatted text. ([#196](https://github.com/davep/rogallo/pull/196))

## v0.11.0

**Released: 2026-07-19**

- Added a `ToggleEmojiRemoval` command to toggle the removal of emoji from
  the content of a page. ([#181](https://github.com/davep/rogallo/pull/181))
- Added a `ToggleANSIEscapeSequenceHandling` command to toggle the
  processing of ANSI escape sequences on and off.
  ([#181](https://github.com/davep/rogallo/pull/181))
- Turning off support for ANSI escape sequences now actually strips all
  sequences. ([#181](https://github.com/davep/rogallo/pull/181))
- Added the ability to change the in-capsule link icon via the configuration
  file. ([#182](https://github.com/davep/rogallo/pull/182))
- Added the ability to change the outwith-capsule link icon via the
  configuration file. ([#182](https://github.com/davep/rogallo/pull/182))
- Added the ability to change the list item bullet icon via the
  configuration file. ([#182](https://github.com/davep/rogallo/pull/182))

## v0.10.0

**Released: 2026-07-18**

- Added support for an optional maximum document width.
  ([#164](https://github.com/davep/rogallo/pull/164))
- Added a link jump progress timeout so numbers typed some time apart don't
  concatenate. ([#167](https://github.com/davep/rogallo/pull/167))
- Added `jump_progress_timeout` to the configuration file to control the
  jump cancellation timeout.
  ([#167](https://github.com/davep/rogallo/pull/167))
- If an input to a capsule fails for some reason, and the user tries to post
  again, the input box is now pre-populated with the failed content for
  further editing. ([#168](https://github.com/davep/rogallo/pull/168))
- Added all application commands to the command line too (in `!snake_case`
  format). ([#169](https://github.com/davep/rogallo/pull/169))
- Added a `GoToParent` command.
  ([#173](https://github.com/davep/rogallo/pull/173))
- Added a `GoToRoot` command.
  ([#173](https://github.com/davep/rogallo/pull/173))
- Added support for signifying if a link in a page has been visited before.
  ([#175](https://github.com/davep/rogallo/pull/175))
- Made the command-palette-based interfaces for history and bookmarks the
  primary interfaces, and turned the previous sidebar-based interfaces into
  secondary "manager" tools.
  ([#176](https://github.com/davep/rogallo/pull/176))

## v0.9.0

**Released: 2026-07-16**

- Added syntax highlighting to pre-formatted text blocks.
  ([#153](https://github.com/davep/rogallo/pull/153))
- Improved the links "stripe" visibility with various themes.
  ([#154](https://github.com/davep/rogallo/pull/154))
- The configuration loading code now filters out settings it doesn't know
  about. ([#155](https://github.com/davep/rogallo/pull/155))
- Added an input length display and guardrail to the user input dialog.
  ([#156](https://github.com/davep/rogallo/pull/156))

## v0.8.0

**Released: 2026-07-15**

- Fixed command line history not recording and recovering correctly.
  ([#143](https://github.com/davep/rogallo/pull/143))
- Added a confirmation step before externally opening unsupported locations or
  MIME types. ([#144](https://github.com/davep/rogallo/pull/144))
- Added keyboard shortcuts to the viewer for easily navigating between each
  of the links, with wrap-around.
  ([#145](https://github.com/davep/rogallo/pull/145))

## v0.7.0

**Released: 2026-07-14**

- Fixed a cosmetic issue with the horizontal truncation of the current
  location as shown in the viewer panel, when it is wider than the viewer.
  ([#131](https://github.com/davep/rogallo/pull/131))
- The command line suggestions now also include all hosts found in the trust
  store. ([#132](https://github.com/davep/rogallo/pull/132))
- Added known hosts from the trust store to the history search palette.
  ([#137](https://github.com/davep/rogallo/pull/137))
- Fixed a cosmetic issue with word-wrapping of the description of a link.
  ([#141](https://github.com/davep/rogallo/pull/141))
- Added support for numeric-based quick jumping to links in the viewer.
  ([#141](https://github.com/davep/rogallo/pull/141))
- Added a `StripeLinks` command to help alternating links stand out better.
  ([#141](https://github.com/davep/rogallo/pull/141))

## v0.6.0

**Released: 2026-07-12**

- Added support for client certificates.
  ([#106](https://github.com/davep/rogallo/pull/106))
- Pages opened from in-page links now bypass the cache.
  ([#106](https://github.com/davep/rogallo/pull/106))
- Fixed a layout issue with list items.
  ([#111](https://github.com/davep/rogallo/pull/111))
- Fixed bookmark search being available when there are no bookmarks to
  search. ([#112](https://github.com/davep/rogallo/pull/112))
- Added `connection_timeout` as a configuration option.
  ([#113](https://github.com/davep/rogallo/pull/113))
- Added `read_timeout` as a configuration option.
  ([#113](https://github.com/davep/rogallo/pull/113))
- Added `maximum_redirects` as a configuration option.
  ([#113](https://github.com/davep/rogallo/pull/113))
- When a page needs a client-side certificate to load, a key icon is shown
  in the viewer's title bar.
  ([#114](https://github.com/davep/rogallo/pull/114))
- Pages that need a client-side certificate are now always excluded from the
  content cache. ([#114](https://github.com/davep/rogallo/pull/114))
- Fixed the way history is recorded so that "post"-type URIs don't end up
  dropping into history and potentially resulting in duplicate inputs being
  sent to capsules. ([#119](https://github.com/davep/rogallo/pull/119))

## v0.5.0

**Released: 2026-07-10**

- Added the MIME type of the document to the viewer's status bar.
  ([#70](https://github.com/davep/rogallo/pull/70))
- Handle showing plain text content without attempting to render it as
  Gemtext. ([#71](https://github.com/davep/rogallo/pull/71))
- Added support for working out the type of a local file when the user goes
  to view it. ([#72](https://github.com/davep/rogallo/pull/72))
- MIME types that can't be handled are all now handed off to the operating
  system's web browser. ([#73](https://github.com/davep/rogallo/pull/73))
- Added the ability to remove individual items from the location history.
  ([#74](https://github.com/davep/rogallo/pull/74))
- Added the ability to clear all locations from the location history.
  ([#74](https://github.com/davep/rogallo/pull/74))
- Added `home_page` to the configuration file.
  ([#75](https://github.com/davep/rogallo/pull/75))
- Added a `GoHome` command.
  ([#75](https://github.com/davep/rogallo/pull/75))
- Added a `SetHome` command.
  ([#75](https://github.com/davep/rogallo/pull/75))
- Added a `SetHomeToCurrentLocation` command.
  ([#75](https://github.com/davep/rogallo/pull/75))
- Added support for bookmarks.
  ([#78](https://github.com/davep/rogallo/pull/78))
- Added navigation history, location history and bookmarks as application
  command line completion suggestions.
  ([#83](https://github.com/davep/rogallo/pull/83))
- Added a `SeachHistory` command.
  ([#86](https://github.com/davep/rogallo/pull/86))
- Adjacent paragraphs in a Gemini document are now consolidated into a
  single widget. ([#91](https://github.com/davep/rogallo/pull/91))
- Cleaned up unnecessary empty lines between quote blocks.
  ([#92](https://github.com/davep/rogallo/pull/92))
- When showing a source view of a page, escape sequences are now shown as
  markup, rather than parsed and rendered.
  ([#94](https://github.com/davep/rogallo/pull/94))
- When a document is loaded, the viewer now automatically gains focus.
  ([#100](https://github.com/davep/rogallo/pull/100))
- Added shortened versions of history, location history and bookmarks as
  application command line completion suggestions.
  ([#103](https://github.com/davep/rogallo/pull/103))
- Added a content cache for content loaded from remote capsules.
  ([#104](https://github.com/davep/rogallo/pull/104))

## v0.4.0

**Released: 2026-06-28**

- Added a `Reload` command.
  ([#58](https://github.com/davep/rogallo/pull/58))
- Added a `CopyLocationToClipboard` command.
  ([#61](https://github.com/davep/rogallo/pull/61))
- Added a `CopyDocumentToClipboard` command.
  ([#61](https://github.com/davep/rogallo/pull/61))
- Added the ability to toggle between a rendered view and a source view.
  ([#62](https://github.com/davep/rogallo/pull/62))
- Added support for user input.
  ([#64](https://github.com/davep/rogallo/pull/64))

## v0.3.0

**Released: 2026-06-26**

- Added a configuration option to turn off link tooltips.
  ([#44](https://github.com/davep/rogallo/pull/44))
- Added a `directories` CLI command to print out the directories used by
  Rogallo. ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `licnece` CLI command to print out the licence details for
  Rogallo. ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `bindings` CLI command to print out the available commands for
  binding to keys, and their default bindings.
  ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `themes` CLI command to print out the available themes.
  ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `--theme` CLI switch for setting the theme.
  ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `--version` CLI switch to print out the version of Rogallo.
  ([#45](https://github.com/davep/rogallo/pull/45))
- Added a `--help` CLI switch to print out the command line help.
  ([#45](https://github.com/davep/rogallo/pull/45))
- Added an `open` CLI command that allows a location to be opened from the
  command line. ([#48](https://github.com/davep/rogallo/pull/48))
- Added support for working with gemtext files in the local filesystem.
  ([#49](https://github.com/davep/rogallo/pull/49))
- Added support for typing scheme-less Gemini URIs into the application's
  command line. ([#51](https://github.com/davep/rogallo/pull/51))
- Added `disable_animations` as a configuration option (disables the default
  Textual animations, for those who might dislike them; which is probably
  anyone with good taste in terminal applications).
  ([#52](https://github.com/davep/rogallo/pull/52))

## v0.2.0

**Released: 2026-06-24**

- Added tooltips to links that show the URI when hovered over with the
  mouse. ([#23](https://github.com/davep/rogallo/pull/23))
- Improved the handling of redirected requests.
  ([#24](https://github.com/davep/rogallo/pull/24))
- Improved the detection of links.
  ([#26](https://github.com/davep/rogallo/pull/26))
- Improved the detection of headings.
  ([#29](https://github.com/davep/rogallo/pull/29))
- Improved the detection of quotes.
  ([#31](https://github.com/davep/rogallo/pull/31))
- Allowed non-standard list items, that use a tab rather than a space after
  the `*`. ([#33](https://github.com/davep/rogallo/pull/33))
- Added a status bar to the viewer widget to show the URI of the
  currently-selected link.
  ([#35](https://github.com/davep/rogallo/pull/35))

## v0.1.0

**Released: 2026-06-23**

- Initial release.

## v0.0.1

**Released: 2026-06-18**

- Initial placeholder package to test that the name is available in PyPI.

[//]: # (ChangeLog.md ends here)
