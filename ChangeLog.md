# Rogallo ChangeLog

## Unreleased

**Released: WiP**

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
