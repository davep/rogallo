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

```python exec="on"
from itertools import chain
from rogallo.widgets.command_line.widget import COMMANDS

for help_line in sorted(chain(*(command.help_text() for command in COMMANDS))):
    _, name, _, _, description, *_ = help_line.split("|")
    if (name := name.strip()).startswith("`!"):
        print(f"- {name}: {description.strip()}")
```

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

Aliases can include template variables (`{q}`, `{qp}`, `{r}`) that are
dynamically replaced by any text typed after the alias name. For example, if
you enter:

```
ken this is a test search
```

`ken` is matched as the alias, and the template variable in the alias definition is replaced using the trailing query string.

The available template variables are:

- `{q}` - The URL-quoted query string (spaces become `%20`).
- `{qp}` - The URL-quoted query string using pluses for spaces (spaces become `+`).
- `{r}` - The raw, unquoted query string.

Given the example above, the template variables expand as follows:

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
type in some text that is the start of a previously-entered input, or
matches known commands, etc, a dimmed completion will be suggested. Press
<kbd>Right</kbd> to accept the suggestion.

```{.textual path="docs/screenshots/main_screenshot.py" title="Showing a suggested completion" lines=40 columns=85 press="/,g,e,m"}
```

[//]: # (command-line.md ends here)
