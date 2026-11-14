# Input Files

Input files provide an alternative method of passing input URLs to gallery-dl
alongside regular command-line arguments.
They are plain-text files containing:

- Input URLs, one per line
- [Options](#options) for those URLs
- [Comments](#comments)

See [docs/options](/docs/options.md#input-options)
for available input file command-line options.


## Options

Any line starting with `-` as its first character
is interpreted as an option name-value pair
that applies to the *next* URL.

These options must be in the form `<NAME> = <VALUE>` where
- `<NAME>` is an option name according to [docs/configuration](/docs/configuration.rst)
- `<VALUE>` is a valid JSON value

Whitespace before and after `=` is optional.

Use `-G` to specify options for *all* following URLs.

```
-G archive = [":~", "gdl", "archives", "{category}"]

- base-directory = "~/gdl/"
https://danbooru.donmai.us/posts/1194245

-    base-directory       = "/tmp/touhou"
-    downloader.http.rate = "1M"
https://danbooru.donmai.us/posts/2434215
```


## Comments

Any line starting with `#` as its first character, or
any text following ` #` after a URL,
is treated as a comment and ignored.

```
# comment-1
https://danbooru.donmai.us/posts/294929
        # ~~ comment-2 ~~
https://danbooru.donmai.us/posts/686612
https://danbooru.donmai.us/posts/5504627  # comment-3
```


## Examples

```
https://x.com/matsu_bouzu
https://x.com/akiko_lawson
https://x.com/pamyurin
```

```
# set global options
-G base-directory = "/tmp/"
-G skip = false

# set local options for the following URL
-filename="spaces_are_optional.jpg"
-skip    = true

https://example.org/

# next URL uses default filename and 'skip' is false.
https://example.com/index.htm # comment1
https://example.com/404.htm   # comment2
```

```
# === Twitter ===
-G cookies = ["firefox", "twitter"]

- include="tweets"
https://x.com/nintendo
- include="videos"
https://x.com/pamyurin
- include=["tweets", "replies"]
- skip = "abort:5"
https://x.com/Pokemon_cojp

# === Instagram ===
-G cookies = ["chrome"]

https://www.instagram.com/cristiano
https://www.instagram.com/therock
```
