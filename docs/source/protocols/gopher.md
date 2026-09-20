# Gopher

## Introduction

Rogallo has support for visiting Gopher servers. Much like when [visiting a
Gemini server](./gemini.md), you can type in the URI of the location you
wish to visit. Gopher URIs begin with `gopher://`.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a Gopher URI" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t"}
```

```{.textual path="docs/screenshots/empty_screenshot.py" title="After pressing Enter" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,enter"}
```

## Supported item types

Rogallo has direct support for a number of Gopher item types. These types
will be handled by or rendered in Rogallo itself. Any other type will be
turned into the most appropriate URI and passed to the operating system to
be handled by other tools.

### `0` - Text

If an item is declared to be text, Rogallo will assume that it is safe to be
treated as a `text/plain` type and, when selected, it will be shown in the
viewer.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Viewing a text file" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,0,/,a,b,o,u,t,.,t,x,t,enter"}
```

### `1` - Menu (directory)

If an item is declared to be a menu, Rogallo will follow the URI.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Viewing another menu" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,1,/,d,o,c,s,enter"}
```

### `7` - Search

If an item is declared to be a search, when selected, Rogallo will prompt
you for the query before following the link.

```{.textual path="docs/screenshots/empty_screenshot.py" title="Entering a search query" lines=30 columns=90 press="g,o,p,h,e,r,:,/,/,l,o,c,a,l,h,o,s,t,:,7,0,7,0,/,enter,4,enter"}
```

### `h` - HTML

If an item is declared as being HTML, and the selector starts with `URL:`,
what follows the `URL:` will be turned into a URI that can be followed.

## Configuration

When showing Gopher maps, Rogallo will optionally prefix lines with a
"badge" related to the type of line. The choices made for each "badge" for
each type might not be to everyone's taste, so you can configure this in the
`gopher.yaml` file found in the [configuration
directory](../configuration/directory.md).

### Default

The default configuration looks like this:

```yaml
show_type_badges: true
type_badges:
  '0': 📄
  '1': 📁
  '2': 📇
  '3': ❌
  '4': 📦
  '5': 💾
  '6': 📜
  '7': 🔍
  '8': 🖥️
  '9': 📦
  I: 🖼️
  P: 📄
  X: 📄
  d: 📄
  g: 🖼️
  h: 🌐
  i: ℹ️
  s: 🎵
  unknown: ❓
```

### Using badges

Item type badges are turned on and used by default. If you wish to turn them
off, set the `show_type_badges` setting to `false`.

```yaml
show_type_badges: false
```

### Configuring badges

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
