# Environment Variables


## `GDL_CONFIG_TYPE`

Specifies file type and filename extension of default configuration files.

Supported since [v1.32.0](https://codeberg.org/mikf/gallery-dl/commit/9fd732afe82f98bc1a592a5078909da366b44957)

### Supported Types
- `json`
- `yaml`
- `toml`

### Command-line Arguments

    --config-type TYPE          Set filetype of default configuration files (json, yaml, toml)


## `GDL_CONFIG_STRICT`

When set, prevents gallery-dl from running
with an invalid default configuration file.

Supported since [v1.32.19](https://codeberg.org/mikf/gallery-dl/commit/8b3f5ee361ee44187b71e310282837be4b1a0a2e)

### Command-line Arguments

    --config-strict             Exit on invalid default configuration files


## `GDL_TEST_RESULTS`

When testing extractor results by running `test/test_results.py`,\
use the results at the given path
instead of the default ones from `test/results`.

Supported since [v1.27.2](https://codeberg.org/mikf/gallery-dl/commit/3eba1f7c293ea86580bce55f84cc2a3f908d0c44)


## `NO_COLOR`

Do not output text with
[ANSI color](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
escape codes by default.\
[https://no-color.org/](https://no-color.org/)

Supported since [v1.27.0](https://codeberg.org/mikf/gallery-dl/commit/dc9d83e64bc15c65100449a48c7390f194cab71e)
