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

## ANSI escape sequence support

Rogallo supports ANSI escape sequences in the content of pages. This means
that sites can do all sorts of wonderfully colourful things:

```{.textual path="docs/screenshots/ansi_screenshot.py" title="Some fun with ANSI" lines=43 columns=80}
```

If you would prefer that ANSI escape sequences *aren't* processed, and
instead a are stripped from the content, you can use the `Toggle ANSI Escape
Sequence Handling` command
([`ToggleANSIEscapeSequenceHandling`](#bindable-commands), bound to
<kbd>Shift</kbd>+<kbd>F6</kbd> by default).

```{.textual path="docs/screenshots/ansi_screenshot.py" title="Turning off ANSI" lines=43 columns=80 press="shift+f6"}
```

Admittedly, in this case the stripped version isn't anywhere near as
interesting, but in most cases you'll get the content you were seeing, just
without colour.

The setting itself is saved in the configuration file as
`handle_ansi_escape_sequences`, which takes `true` or `false` as valid
values. It will be `true` (handle ANSI sequences) by default:

```json
"handle_ansi_escape_sequences": true
```

## Bookmarks manager visible

Rogallo has a sidebar that displays the bookmarks manager. By default it
isn't visible. It can be made visible with the `Toggle Bookmarks Manager`
command ([`ToggleBookmarks`](#bindable-commands), bound to <kbd>F3</kbd> by
default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo with the bookmarks manager visible" lines=35 columns=90 press="shift+f3"}
```

The setting itself is saved in the configuration file as
`bookmarks_visible`, which takes `true` or `false` as valid values. It will
be `false` (not visible) by default:

```json
"bookmarks_visble": false
```

## Connection settings

Rogallo imposes some limits on connections to capsules. These include the
connection timeout, the read timeout and the maximum number of redirects
that will be handled. If you wish to modify these you can change the
following values:

```json
"connection_timeout": 10,
"read_timeout": 30,
"maximum_redirects": 5,
```

`connection_timeout` and `read_timeout` are an integer number of seconds.
`maximum_redirects` is an integer number of redirections that will be
followed.

## Content cache

Rogallo uses a content cache to make some forms of navigation between pages
faster, reducing the need to connect to a capsule and download data. The
`cache_ttl` configuration setting controls how long a cache entry is used
before it is considered stale. This is an integer number of seconds, set to
`3600` (1 hour) by default.

```json
"cache_ttl": 3600
```

If you would prefer to not use a cache at all, this can be turned off via
the `with_cache` setting. Value values are `true` and `false`, set to `true`
by default.

```json
"with_cache": true
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

## Emoji removal

Some people find the use of emoji in Gemtext off-putting. Rogallo has a
configuration option for those people. The `Toggle Emoji Removal` command
([`ToggleEmojiRemoval`](#bindable-commands), bound to <kbd>F6</kbd> by
default) can be used to clean things up.

So, if presented with this:

```{.textual path="docs/screenshots/emoji_screenshot.py" title="Lots of emoji" lines=30 columns=80}
```

you can run the command and the content will look more like this:

```{.textual path="docs/screenshots/emoji_screenshot.py" title="Cleaned of emoji" lines=30 columns=80 press="f6"}
```

The setting itself itself is saved in the configuration file as the
`strip_emoji` configuration setting. It accepts `true` or `false` as valid
values. It will be `false` (don't remove) by default.

```json
"strip_emoji": false
```

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

## History manager visible

Rogallo has a sidebar that displays the history manager. By default it isn't
visible. It can be made visible with the `Toggle History` command
([`ToggleHistoryManager`](#bindable-commands), bound to <kbd>F2</kbd> by default).

```{.textual path="docs/screenshots/main_screenshot.py" title="Rogallo with the history manager visible" lines=50 columns=120 press="shift+f2"}
```

The setting itself is saved in the configuration file as `history_visible`,
which takes `true` or `false` as valid values. It will be `false` (not
visible) by default:

```json
"history_visble": false
```

## Home page

Rogallo has a home page setting. This can be set using the `Set Home`
command ([`SetHome`](#bindable-commands) command, bound to
<kbd>Alt</kbd>+<kbd>h</kbd> by default). This sets the currently-visited
page as the home page. If you wish you can also modify it in the
configuration file:

```json
"home_page": "gemini://geminiprotocol.net/"
```

## Icons

Three main "icons" are used within a rendered document:

- Links within a Gemini capsule
- Links outwith a Gemini capsule
- List item bullet

If, for any reason, you don't like the character choices made by Rogallo for
these icons, you can modify these values in the configuration file:

```json
"geminispace_link_icon": "\u2aa2",
"otherspace_link_icon": "\u2197",
"list_item_bullet_icon": "\u2022"
```

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

## Link jumps

In Rogallo, you can navigate to links using <kbd>Tab</kbd> and
<kbd>Shift</kbd>+<kbd>Tab</kbd> (the method of navigating between most UI
elements in the application), and you can also use the mouse. Sometimes,
though, if there's lots of links, it's handy to be able to jump straight to
a link. To this end Rogallo provides numeric labels:

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links with labels" lines=30 columns=70}
```

When the viewer is focused, if you type the number of a link, that link will
be highlighted:

```{.textual path="docs/screenshots/stripes_screenshot.py" title="A highlighted link after typing its number" lines=30 columns=70 press="5"}
```

If anyone finds this distracting, you can turn the labels off with the
`Toggle Link Numbers` ([`ToggleLinkNumbers`](#bindable-commands), bound to
<kbd>Shift</kbd>+<kbd>F8</kbd> by default) command.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Link number jumps turned off" lines=30 columns=70 press="shift+f8"}
```

The setting itself is saved in the configuration file as the
`with_link_jumps`configuration setting. It accepts `true` or `false` as
valid values. It will be `true` (with labels) by default.

```json
"with_link_jumps": true
```

## Link tooltips

By default, when using a mouse, Rogallo will show a tooltip containing the
target URI when you hover the mouse cursor over a link.

```{.textual path="docs/screenshots/links_screenshot.py" title="Rogallo showing a link tooltip" lines=35 columns=90 hover="GemtextLink"}
```

If this feels too cluttered it can be turned off with the
`show_link_tooltips` setting. Valid values are `true` and `false`, with
`true` (show the tooltips) being the default.

```json
"show_link_tooltips": true
```

## Maximum document width

By default a document being displayed in Rogallo will take up as much
horizontal width as possible. So, if the terminal is 80 characters wide,
it'll look like this:

```{.textual path="docs/screenshots/max_width_off_screenshot.py" title="Text at 80 characters wide" lines=40 columns=80}
```

At 120:

```{.textual path="docs/screenshots/max_width_off_screenshot.py" title="Text at 120 characters wide" lines=60 columns=120}
```

And even wider:

```{.textual path="docs/screenshots/max_width_off_screenshot.py" title="Text at 430 characters wide" lines=215 columns=430}
```

If you prefer that Rogallo always caps the width of text at a specific
value, set `maximum_document_width` in the configuration file. A value of
`0` means "no limit" (the default value). If you would prefer that it's set
to 80 characters, for example:

```json
"maximum_document_width": 80
```

```{.textual path="docs/screenshots/max_width_on_screenshot.py" title="Document widget capped at 80 characters wide" lines=60 columns=120}
```

## Pre-formatted text tooltips

By default, when using a mouse, Rogallo will show any alt-text associated
with some pre-formatted text when you hover the mouse cursor over the block
of text.

```{.textual path="docs/screenshots/preformat_screenshot.py" title="Rogallo showing a pre-format tooltip" lines=35 columns=90 hover="GemtextPreformatted:last-of-type"}
```

If this feels too cluttered it can be turned off with the
`show_preformat_tooltips` setting. Valid values a `true` and `false`, with
`true` (show the tooltips) being the default.

```json
"show_preformat_tooltips": true,
```

## Striped links

Rogallo provides a method of quick-jumping to links that is based around
numeric labels that appear on the right in the viewer area. Placing the
labels to the right helps keep a readable flow of text, but can possibly
make it trickier to know which label matches which link.

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links and labels with no stripes" lines=30 columns=70}
```

To help with this you can turn on "striped links", which alternates the
background colour of links to help make them stand out and connect with
their labels. This is toggled using the `Stripe Links`
([`StripeLinks`](#bindable-commands) command, bound to <kbd>F8</kbd> by
default).

```{.textual path="docs/screenshots/stripes_screenshot.py" title="Links with stripes" lines=30 columns=70 press="f8"}
```

The setting itself is saved in the configuration file as the `strike_links`
configuration setting. It accepts `true` or `false` as valid values. It will
be `false` (no stripes) by default:

```json
"stripe_links": false
```

## Theme

Rogallo has a number of themes available. You can select a theme using the
`Change Theme` ([`ChangeTheme`](#bindable-commands) command, bound to
<kbd>F9</kbd> by default) command. The available themes include:

```bash exec="on"
rogallo themes | sed 's/^/- /'
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
