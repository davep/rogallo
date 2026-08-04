# The command line

## Introduction

The command line is used to enter URIs and commands. These are covered in
here, but if you need help with what's available while you're using Rogallo,
you can always request help by entering `?` in the command line, or calling
on the `Help` command (bound to <kbd>F1</kbd> by default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Command line help" lines=70 columns=140 press="/,f1"}
```

## URIs

If you wish to type in a location to visit, the command line is where you do
this. What you type will depend on the [protocol](./protocols.md) you're
working with. Generally they will be:

- **Gemini**: `gemini://example.com/`
- **Gopher**: `gopher://example.com/`
- **Finger**: `finger://example.com/davep`
- **Files**: `file:///path/to/file.txt`

If an entered value isn't obviously a URI, and isn't a known command or
[alias](#aliases), it is treated as follows:

- If it is a path to an existing file in the local file system, that file
  will be turned into a URI and an attempt will be made to open it.
- If it is a path to an existing directory in the local file system, that
  directory will be opened in a file-opening dialog, allowing you to browse
  for and select a file to view.
- Otherwise, it will be turned into a `gemini://` URL and will be processed
  as such.

So, in most cases, if you enter `example.com`, it will be opened as
`gemini://example.com/`.

## Commands

Commands start with a `!`. The commands include:

- `!about_this_page`: Show information about the current page
- `!add_location_to_bookmarks`: Add the current location to the bookmarks
- `!backward`: Move backward through history
- `!change_command_line_location`: Swap the position of the command line between top and bottom
- `!clear_cache`: Clear the cache for all content
- `!copy_document_to_clipboard`: Copy the current document to the clipboard
- `!copy_location_to_clipboard`: Copy the current location to the clipboard.
- `!finger <user>@<host>`: Perform user information looking with the finger protocol
- `!forward`: Move forward through history
- `!go_home`: Go to the home page
- `!go_to_parent`: Go to the parent directory
- `!go_to_root`: Go to the root directory
- `!help`: Show the help screen
- `!jump_to_command_line`: Jump to the command line
- `!jump_to_document`: Jump to the document viewer
- `!jump_to_sidebar`: Jump to the sidebar
- `!open_file`: Open a file in the local filesystem
- `!quit`: Quit the application
- `!reload`: Reload the current document
- `!search_bookmarks`: Search the bookmarks for a location
- `!search_history`: Search the history for a location
- `!set_home_to_current_location`: Set the home page to the current location
- `!set_home`: Set the home page to a specific location
- `!stripe_links`: Toggle the striping of links in the document viewer
- `!theme`: Change the application theme
- `!toggle_ansi_escape_sequence_handling`: Toggle the handling of ANSI escape sequences in text content
- `!toggle_bookmarks_manager`: Toggle the display of the bookmarks viewer
- `!toggle_cosy_link_numbers`: Toggle the position of link numbers when they're being displayed
- `!toggle_emoji_removal`: Toggle the removal of emoji from text content
- `!toggle_history_manager`: Toggle the display of the history viewer
- `!toggle_link_numbers`: Toggle the display of link numbers in the document viewer
- `!toggle_view`: Toggle between rendered and source view of the document

## Aliases

Rogallo supports a simple form of aliases for its command line. Primarily
they're useful for defining things such as performing searches using popular
Gemini and Gopher search engines. Aliases are defined in the [configuration
file](./configuration.md), like this:

```json
"aliases": {
    "fg": "gopher://gopher.floodgap.com/1/v2/vs?{q}",
    "gp": "gemini://gemi.dev/cgi-bin/wp.cgi/search?{q}",
    "ken": "gemini://kennedy.gemi.dev/search?{q}",
    "tlgs": "gemini://tlgs.one/search?{q}"
}
```

As you may notice, a form of template label is used. The substitution is
always whatever follows the command input into the command line. So if you
were to type in :

```
ken this is a test search
```

`ken` would be matched as a command alias, and the template label would be
some form of `this is a test search`. The available template labels are:

- `{q}` - The string, quoted. Spaces become `%20`, etc.
- `{qp}` - As above, but spaces specifically become `+` rather than `%20`.
- `{r}` - The raw, unquoted, version of the text.

So, given the above example, the expansions would be:

- `{q}` -> `this%20is%20a%20test%20search`
- `{qp}` -> `this+is+a+test+search`
- `{r}` -> `this is a test search`

While the default set of aliases all expand into URIs, which perform
searches with search engines, this isn't the only application. For example,
if you preferred to type `whois` rather than `!finger` to call on a finger
server, you could have:

```json
"whois": "!finger {r}"
```

## History and completion

Rogallo's command line has a simple history system. As you type commands,
they are recorded in the command line history and are kept available between
sessions. You can use the <kbd>Up</kbd> and <kbd>Down</kbd> keys to navigate
through the command history.

The command line also has a simple suggested completion system too. If you
type in some text that is the start if a previously-entered input, or
matches known commands, etc, a dimmed completion will be suggested. Press
<kbd>Right</kbd> to accept the suggestion.

```{.textual path="docs/screenshots/main_screenshot.py" title="Showing a suggested completion" lines=40 columns=85 press="/,g,e,m"}
```

[//]: # (command-line.md ends here)
