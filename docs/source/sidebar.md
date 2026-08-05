# The sidebar

## Introduction

Rogallo can optionally show a sidebar widget containing either your bookmarks or
your location history. By default, the sidebar is hidden. It operates on a
toggle basis depending on focus and current visibility. If it is hidden, running
either `ToggleBookmarksManager` (bound to <kbd>Shift</kbd>+<kbd>F3</kbd> by default)
or `ToggleHistoryManager` (bound to <kbd>Shift</kbd>+<kbd>F2</kbd> by default)
will open it.

```{.textual path="docs/screenshots/main_screenshot.py" title="The bookmarks manager" lines=40 columns=80 press="shift+f3"}
```

```{.textual path="docs/screenshots/main_screenshot.py" title="The history manager" lines=40 columns=80 press="shift+f2"}
```

## Bookmarks manager

The bookmarks manager allows you to view, edit, and remove your bookmarks.
Calling the `ToggleBookmarksManager` command operates as a contextual toggle:

- **Sidebar closed**: Opens the sidebar showing the bookmarks manager.
- **Sidebar open (unfocused)**: Focuses the sidebar and displays the bookmarks manager.
- **Sidebar open (focused on history)**: Switches the sidebar display to the bookmarks manager.
- **Sidebar open (focused on bookmarks)**: Closes the sidebar.

While bookmarks are visible and focused the following keys perform the
following actions:

- `d` - Delete the highlighted bookmark.
- `r` - Rename the highlighted bookmark.

## History manager

The history manager allows you to view and delete your browsing history.
Calling the `ToggleHistoryManager` command operates as a contextual toggle:

- **Sidebar closed**: Opens the sidebar showing the history manager.
- **Sidebar open (unfocused)**: Focuses the sidebar and displays the history manager.
- **Sidebar open (focused on bookmarks)**: Switches the sidebar display to the history manager.
- **Sidebar open (focused on history)**: Closes the sidebar.

While history is visible and focused the following keys perform the
following actions:

- `d` - Delete the highlighted history item.
- `D` - Remove all history items.

[//]: # (sidebar.md ends here)
