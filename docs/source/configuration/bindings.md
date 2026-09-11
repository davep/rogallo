# Keyboard bindings

Rogallo allows for a degree of configuration of its keyboard bindings;
providing a method for setting up replacement bindings for the commands that
appear in the [command palette](../index.md#the-command-palette).

## Bindable commands

The following commands can have their keyboard bindings set:

```bash exec="on"
rogallo bindings | sed -e 's/^\([A-Z].*\) - \(.*\)$/- `\1` - *\2*/' -e 's/^    \(Default:\) \(.*\)$/    - *\1* `\2`/'
```

## Changing a binding

Rogallo's default bindings for all of the above commands can be overridden
using a `bindings.yaml` file placed in the [configuration directory](./index.md).

!!! tip

    The configuration directory will be below [`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/),
    in a `rogallo` subdirectory. Mostly this will translate to the directory being
    called `~/.config/rogallo/`.

If you wish to change the binding for a command, create the `bindings.yaml`
file in the configuration directory (if it doesn't already exist), and add a
line in the format:

```yaml
<Command>: <Key>
```

where `<Command>` is a recognised Rogallo command and `<Key>` is the key to
bind to it. For example, if you wanted to change the binding used to toggle
the display of a page between a rendered view or a source view, changing it
from <kbd>f4</kbd> to <kbd>ctrl</kbd>+<kbd>t</kbd>, you would add this:

```yaml
ToggleView: "ctrl+t"
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

A fuller example of a custom keyboard binding file might look like:

```yaml
Backward: "ctrl+h"
Forward: "ctrl+l"
ToggleView: "ctrl+t"
GoHome: "ctrl+shift+h"
```

[//]: # (bindings.md ends here)
