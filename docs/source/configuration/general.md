# General configuration

The following settings can be configured in `general.yaml` in the
[configuration directory](./directory.md).

## Connection settings

Rogallo imposes some limits on connections to capsules and other data
sources. These include the connection timeout, the read timeout and the
maximum number of redirects that will be handled. If you wish to modify
these you can change the following values:

```yaml
connection_timeout: 10,
read_timeout: 30,
maximum_redirects: 5,
```

`connection_timeout` and `read_timeout` are an integer number of seconds.
`maximum_redirects` is an integer number of redirections that will be
followed.

## Content cache

Rogallo uses a content cache to make some forms of navigation between pages
faster, reducing the need to connect to a host and download data. The
`cache_ttl` configuration setting controls how long a cache entry is used
before it is considered stale. This is an integer number of seconds, set to
`3600` (1 hour) by default.

```yaml
cache_ttl: 3600
```

If you would prefer to not use a cache at all, this can be turned off via
the `with_cache` setting. Valid values are `true` and `false`, set to `true`
by default.

```yaml
with_cache: true
```

## Disable animations

Rogallo is built using the [Textual
framework](https://textual.textualize.io/). Textual has a tendency to go
overboard with animations when scrolling content. Some people like this,
some don't. For some it's an accessibility issue. If you would prefer that
such animations are disabled, set the `disable_animations` configuration
setting. It accepts `true` or `false` as valid values. It will be `false`
(use animations) by default:

```yaml
disable_animations: false
```

## User input editor

Rogallo supports using your choice of external text editor to edit user
input. By default the input dialog will look to see if `$VISUAL` or
`$EDITOR` are set in the environment and, if they are, you can press
<kbd>F3</kbd> when editing input to open your editor.

If you would prefer to set a specific editor for Rogallo itself, you can set
`external_editor` in the configuration file. By default it is `null` (in
which case it will look for `$VISUAL` and then `$EDITOR`):

```yaml
external_editor: null
```

Set it to the program to run to use that specific editor for Rogallo.

[//]: # (general.md ends here)
