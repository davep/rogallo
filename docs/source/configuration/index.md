# Introduction

The way that Rogallo works can be configured using a configuration file.
This section will describe what can be configured and how.

Most configuration is done in a file called `configuration.json`, which
lives in [Rogallo's configuration directory](./directory.md).

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

[//]: # (configuration.md ends here)
