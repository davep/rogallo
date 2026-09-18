# The side panel

## Introduction

Rogallo has a side panel that can be opened and closed using the
`ToggleSidePanel` command (bound to <kbd>Ctrl</kbd>+<kbd>l</kbd> by
default). It contains the [bookmarks manager](#bookmarks-manager), [history
manager](#history-manager) and the [client certificates
manager](#client-certificates-manager).

```{.textual path="docs/screenshots/main_screenshot.py" title="The side panel popped open" lines=40 columns=100 press="ctrl+l"}
```

## Left/right dock

You can control if the side panel docks to the left or right of the screen.
When focus is within the side panel, use either of:

- `[` - Dock the side panel to the left
- `]` - Dock the side panel to the right

## Bookmarks manager

The bookmarks manager allows you to view, edit, and remove your bookmarks.
While the bookmarks tab is selected the following keys perform the following
actions:

- `d` - Delete the highlighted bookmark
- `r` - Rename the highlighted bookmark

## History manager

The history manager allows you to view and delete your browsing history.
While the history tab is selected the following keys perform the following
actions:

- `d` - Delete the highlighted history item
- `D` - Remove all history items

## Client certificates manager

The client certificate manager allows you to create, associate, disassociate
and remove Gemini client certificates. While the certificate tab is selected
the following keys perform the following actions:

- `n` - Create a new client certificate
- `d` - Delete a client certificate
- `a` - Associate the highlighted certificate with a Gemini URI
- `r` - Remove an association from the highlighted certificate
- `x` - Export the highlighted certificate
- `i` - Import a certificate
- `v` - View the details of the highlighted certificate

## Available bindings

The following actions can [have their bindings overridden](../configuration/bindings.md):

### Main panel

- `side_panel.switch_previous_tab` - Switch to the previous tab
- `side_panel.switch_next_tab` - Switch to the next tab
- `side_panel.dock_left` - Dock the side panel to the left of the terminal
- `side_panel.dock_right` - Dock the side panel to the right of the terminal

### Bookmarks manager

- `bookmarks.delete` - Delete the highlighted bookmark
- `bookmarks.rename` - Rename the highlighted bookmark

### History manager

- `history.delete_all_locations` - Remove all history items
- `history.delete_location` - Delete the highlighted history item

### Client certificates manager

- `client_certificates.add_association` - Associate the highlighted certificate with a Gemini URI
- `client_certificates.delete` - Delete a client certificate
- `client_certificates.export` - Export the highlighted certificate
- `client_certificates.import`- Import a certificate
- `client_certificates.new` - Create a new client certificate
- `client_certificates.remove_association` - Remove an association from the highlighted certificate
- `client_certificates.view` - View the details of the highlighted certificate

[//]: # (side-panel.md ends here)
