# Configuration directory

## Location

Rogallo's configuration directory lives below
[`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/),
in a `rogallo` subdirectory. Mostly this will translate to the directory
being called `~/.config/rogallo/`.

If you are unsure of the location you can use [the `directories`
command](../index.md#directories).

```sh
$ rogallo directories

/Users/davep/.cache/rogallo
/Users/davep/.config/rogallo
/Users/davep/.local/share/rogallo
```

## Contents

The usual contents of the configuration directory are:

- [`aliases.yaml`](../ui/command-line.md#aliases)
- [`bindings.yaml`](./bindings.md)
- [`configuration.json`](./index.md)
- [`themes/*.json`](../ui/custom-themes.md)

[//]: # (directory.md ends here)
