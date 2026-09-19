# Introduction

The way that Rogallo works can be configured using a configuration file.
This section will describe what can be configured and how.

Most configuration is done in a file called `configuration.json`, which
lives in [Rogallo's configuration directory](./directory.md).

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
the `with_cache` setting. Valid values are `true` and `false`, set to `true`
by default.

```json
"with_cache": true
```

## Command line position

By default, Rogallo's command line appears at the bottom of the screen,
above the footer of the application. It can be moved to the top of the
screen, below the application header, with the `Change Command Line
Location` command ([`ChangeCommandLineLocation`](bindings.md#bindable-commands), bound
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

## Home page

Rogallo has a home page setting. This can be set using the `Set Home`
command ([`SetHome`](bindings.md#bindable-commands), bound to
<kbd>Alt</kbd>+<kbd>h</kbd> by default). This sets the currently-visited
page as the home page. If you wish you can also modify it in the
configuration file:

```json
"home_page": "gemini://geminiprotocol.net/"
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

## Theme

Rogallo has a number of themes available. You can select a theme using the
`Change Theme` ([`ChangeTheme`](bindings.md#bindable-commands) command, bound to
<kbd>F9</kbd> by default) command. The available themes include:

```bash exec="on"
rogallo themes | grep -v "\(terminal\|micro\)-" | sed 's/^/- /'
```

!!! tip

    You can also [set the theme via the command line](../index.md#-t-theme). This can
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

## User input editor

Rogallo supports using your choice of external text editor to edit user
input. By default the input dialog will look to see if `$VISUAL` or
`$EDITOR` are set in the environment and, if they are, you can press
<kbd>F3</kbd> when editing input to open your editor.

If you would prefer to set a specific editor for Rogallo itself, you can set
`external_editor` in the configuration file. By default it is `null` (in
which case it will look for `$VISUAL` and then `$EDITOR`):

```json
"external_editor": null
```

Set it to the program to run to use that specific editor for Rogallo.

[//]: # (configuration.md ends here)
