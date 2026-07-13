# Introduction

The way that Rogallo works can be configured using a configuration file.
This section will describe what can be configured and how.

The location of the configuration file will depend on how your operating
system and its settings; but by default it is looked for in
[`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/),
in a `rogallo` subdirectory. Mostly this will translate to the file being
called `~/.config/rogallo/configuration.json`.

!!! tip

    You can discover the exact directory with the [`directories` command
    line command](index.md#directories)

## Bookmarks visible

Rogallo has a sidebar that displays the bookmarks you've saved. By default
it isn't visible. It can be made visible with the `Toggle Bookmarks` command
([`ToggleBookmarks`](#bindable-commands), bound to <kbd>F3</kbd> by
default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo with the command line on top" lines=35 columns=90 press="f3"}
```

The setting itself is saved in the configuration file as
`bookmarks_visible`, which takes `true` or `false` as valid values. It will
be `false` (not visible) by default:

```json
"bookmarks_visble": false
```

## Command line position

By default, Rogallo's command line appears at the bottom of the screen,
above the footer of the application. It can be moved to the top of the
screen, below the application header, with the `Change Command Line
Location` command ([`ChangeCommandLineLocation`](#bindable-commands), bound
to <kbd>Ctrl</kbd>+<kbd>Up</kbd> by default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo with the command line on top" lines=35 columns=90 press="ctrl+up,ctrl+1"}
```

The setting itself is saved in the configuration file as
`command_line_on_top`, which takes `true` or `false` as valid values. It
will be `false` (at the bottom) by default:

```json
"command_line_on_top": false
```

## Disable animations

Rogallo is built using the [Textual
framework](https://textual.textualize.io/). Textual has a tendency to go
overboard with animations when scrolling content. Some people like this,
some don't. For some it's an accessibility issue. If you would prefer that
such animations are disabled, set the `disable_animations` configuration
setting. It accepts `true` or `false` as valid values. It will be `false`
(use animations) by default:

```json
"disable_animations": false
```

## Displayable content types

By default Rogallo only considers a narrow set of MIME types as displayable
in the application. In the event that you need to expand this list, you can
change the value of `displayable_content_types`:

```json
"displayable_content_types": [
    "text/gemini",
    "text/plain"
]
```

!!! important

    Rogallo is currently only capable of displaying text-based content,
    showing either rendered Gemtext or plain text. Adding other MIME types
    might cause unwanted or unpredictable results.

## Handling ANSI escape sequences

Some Gemini capsules have content -- sometimes optional, sometimes mandatory
-- which makes use of ANSI escape sequences to add colour to a document.
Rogallo supports this and will accept and correctly render the sequences.

If you would prefer that Rogallo *didn't* handle server-supplied escape
sequences you can turn it off with the `handle_ansi_escape_sequences`
setting. It takes `true` and `false` as valid values, and is `true` by
default.

```json
"handle_ansi_escape_sequences": true
```

!!! note

    Turning this off and visiting sites that still deliver escape sequences
    will have unpredictable results.

## Keyboard bindings

Rogallo allows for a degree of configuration of its keyboard bindings;
providing a method for setting up replacement bindings for the commands that
appear in the [command palette](index.md#the-command-palette).

### Bindable commands

The following commands can have their keyboard bindings set:

```bash exec="on"
rogallo bindings | sed -e 's/^\([A-Z].*\) - \(.*\)$/- `\1` - *\2*/' -e 's/^    \(Default:\) \(.*\)$/    - *\1* `\2`/'
```

### Changing a binding

If you wish to change the binding for a command, edit the configuration file
and add the binding to the `bindings` value. For example, if you wanted to
change the binding used to toggle the display of a page between a rendered
view or a source view, changing it from <kbd>f4</kbd> to
<kbd>ctrl</kbd>+<kbd>t</kbd>, you would set `bindings` to this:

```json
"bindings": {
    "ToggleView": "ctrl+t"
}
```

The designations used for keys is based on the internal system used by
[Textual](https://textual.textualize.io); as such [its caveats about what
works where
apply](https://textual.textualize.io/FAQ/#why-do-some-key-combinations-never-make-it-to-my-app).
The main modifier keys to know are `shift`, `ctrl`, `alt`, `meta`, `super`
and `hyper`; letter keys are their own letters; shifted letter keys are
their upper-case versions; function keys are simply <kbd>f1</kbd>,
<kbd>f2</kbd>, etc; symbol keys (the likes of `#`, `@`, `*`, etc...)
generally use a name (`number_sign`, `at`, `asterisk`, etc...).

!!! tip

    If you want to test and discover all of the key names and combinations
    that will work, you may want to install
    [`textual-dev`](https://github.com/Textualize/textual-dev) and use the
    `textual keys` command.

    If you need help with keyboard bindings [please feel free to
    ask](index.md#questions-and-feedback).

## Theme

Rogallo has a number of themes available. You can select a theme using the
`Change Theme` ([`ChangeTheme`](#bindable-commands) command, bound to
<kbd>F9</kbd> by default) command. The available themes include:

```bash exec="on"
dhv themes | sed 's/^/- /'
```

!!! tip

    You can also [set the theme via the command line](index.md#-t-theme). This can
    be useful if you want to ensure that Rogallo runs up with a specific theme.
    Note that this *also* configures the theme for future runs of Rogallo.

Here's a sample of some of the themes:

```{.textual path="docs/screenshots/main_screenshot.py" title="textual-light" lines=35 columns=90 press="f9,t,e,x,t,u,a,l,-,l,i,g,h,t,enter"}
```

```{.textual path="docs/screenshots/main_screenshot.py" title="nord" lines=35 columns=90 press="f9,n,o,r,d,enter"}
```

```{.textual path="docs/screenshots/main_screenshot.py" title="catppuccin-latte" lines=35 columns=90 press="f9,c,a,t,p,p,u,c,c,i,n,-,l,a,t,t,e,enter"}
```

```{.textual path="docs/screenshots/main_screenshot.py" title="dracula" lines=35 columns=90 press="f9,d,r,a,c,u,l,a,enter"}
```

[//]: # (configuration.md ends here)
