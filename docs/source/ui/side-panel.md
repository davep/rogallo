# The side panel

## Introduction

Rogallo has a side panel that can be opened and closed using the
`ToggleSidePanel` command (bound to <kbd>Ctrl</kbd>+<kbd>l</kbd> by
default). It contains the [bookmarks manager](#bookmarks-manager), [history
manager](#history-manager) and the [client certificates
manager](#client-certificates-manager).

```{.textual path="docs/screenshots/main_screenshot.py" title="The side panel popped open" lines=40 columns=100 press="ctrl+l"}
```

## Bookmarks manager

The bookmarks manager allows you to view, edit, and remove your bookmarks.
While the bookmarks tab is selected the following keys perform the following
actions:

- `d` - Delete the highlighted bookmark.
- `r` - Rename the highlighted bookmark.

## History manager

The history manager allows you to view and delete your browsing history.
While the history tab is selected the following keys perform the following
actions:

- `d` - Delete the highlighted history item.
- `D` - Remove all history items.

## Client certificates manager

The client certificate manager allows you to create, associate, disassociate
and remove Gemini client certificates. While the certificate tab is selected
the following keys perform the following actions:

- `n` - Create a new client certificate.
- `d` - Delete a client certificate.
- `a` - Associate the highlighted certificate with a Gemini URI.
- `r` - Remove an association from the highlighted certificate.
- `x` - Export the highlighted certificate.
- `i` - Import a certificate.

## Configuration

### Left or right side

By default the Rogallo side panel is on the left side of the screen. If you
would prefer that it's on the right side, you can modify the
`side_panel_on_right` setting in the configuration file:

```json
"side_panel_on_right": false
```

Set it to `true` to position the side panel on the right.

[//]: # (side-panel.md ends here)
