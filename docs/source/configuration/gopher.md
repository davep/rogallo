# Gopher

When showing [Gopher](../protocols/gopher.md) maps Rogallo will optionally
prefix lines with a "badge" related to the type of line. The choices made
for each "badge" for each type might not be to everyone's taste, so you can
configure this in the `gopher.yaml` file found in the [configuration
directory](./index.md).

## Default

The default configuration looks like this:

```yaml
show_type_badges: true
type_badges:
  '0': "\U0001F4C4"
  '1': "\U0001F4C1"
  '2': "\U0001F4C7"
  '3': "\u274C"
  '4': "\U0001F4E6"
  '5': "\U0001F4BE"
  '6': "\U0001F4DC"
  '7': "\U0001F50D"
  '8': "\U0001F5A5\uFE0F"
  '9': "\U0001F4E6"
  I: "\U0001F5BC\uFE0F"
  P: "\U0001F4C4"
  X: "\U0001F4C4"
  d: "\U0001F4C4"
  g: "\U0001F5BC\uFE0F"
  h: "\U0001F310"
  i: "\u2139\uFE0F"
  s: "\U0001F3B5"
  unknown: "\u2753"
```

## Using badges

Item type badges are turned on and used by default. If you wish to turn them
off, set the `show_type_badges` setting to `false`.

```yaml
show_type_badges: false
```

## Configuring badges

You can control what is shown for each badge. By default the values are
various characters themed after the types. If you wish to show different
text, change the values for each defined type. For example, if you wanted to
use simple three-latter codes:

```yaml
type_badges:
  '0': "(TXT)"
  '1': "(DIR)"
  '2': "(CSO)"
  '3': "(ERR)"
  '4': "(HQX)"
  '5': "(DOS)"
  '6': "(UUE)"
  '7': "(FND)"
  '8': "(TEL)"
  '9': "(BIN)"
  I: "(IMG)"
  P: "(PDF)"
  X: "(XML)"
  d: "(DOC)"
  g: "(BIN)"
  h: "(WEB)"
  i: "(INF)"
  s: "(SND)"
  unknown: "(???)"
```

[//]: # (gopher.md ends here)
