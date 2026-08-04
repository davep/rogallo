# The sidebar

## Introduction

Rogallo can optionally show a sidebar widget, which contains either your
bookmarks or your location history. By default the sidebar isn't visible, it
shows on a toggle basis, depending on where focus is and what's currently
visible. If it isn't visible and you run either of `ToggleBookmarksManager`
(bound to <kbd>Shift</kbd>+<kbd>F3</kbd> by default) or
`ToggleHistoryManager` (bound to <kbd>Shift</kbd>+<kbd>F2</kbd> by default)
it will appear.

```{.textual path="docs/screenshots/main_screenshot.py" title="The bookmarks manager" lines=40 columns=80 press="shift+f3"}
```

```{.textual path="docs/screenshots/main_screenshot.py" title="The history manager" lines=40 columns=80 press="shift+f2"}
```

## Bookmarks manager

The bookmarks manager can be used to view, edit and remove your bookmarks.
Calling the `ToggleBookmarksManager` command will do one of the following
things:

- If the sidebar isn't open, it will be opened and the bookmark manager will
  be shown.
- If the sidebar is open but doesn't have focus, focus will be moved to the
  sidebar and the bookmarks will be shown.
- If the sidebar is open and it has focus and the bookmarks aren't shown,
  the content will swap to the bookmarks.
- If the sidebar is open and focused and the bookmarks are shown, the
  sidebar will be closed.

While bookmarks are visible and focused the following keys perform the
following actions:

- `d` - Delete the highlighted bookmark.
- `r` - Rename the highlighted bookmark.

## History manager

The history manager can be used to view and delete your history. Calling the
`ToggleHistoryManager` command will do one of the following things:

- If the sidebar isn't open, it will be opened and the history manager will
  be shown.
- If the sidebar is open but doesn't have focus, focus will be moved to the
  sidebar and the history will be shown.
- If the sidebar is open and it has focus and the history isn't shown, the
  content will swap to the history.
- If the sidebar is open and focused and the history is shown, the sidebar
  will be closed.

While history is visible and focused the following keys perform the
following actions:

- `d` - Delete the highlighted history item.
- `D` - Remove all history items.

[//]: # (sidebar.md ends here)
