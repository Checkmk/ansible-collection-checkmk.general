# Integration Tests

One target per module (`tests/integration/targets/<name>/`) or lookup
plugin (`tests/integration/targets/lookup_<name>/`). Every target depends
on the `setup_checkmk` role, which installs and starts the Checkmk site(s)
the tests run against.

## Running

```bash
uv run ansible-test integration --docker                        # full suite
uv run ansible-test integration <target> --docker                # single target, e.g. host
uv run ansible-test integration <target> <target2> --docker      # a few targets
uv run ansible-test integration --start-at <target> --docker     # resume after a failure
```

`--docker` must come last, after any target names.

By default this installs Checkmk into a single container and
creates a central site (`testsite`, port 5000) plus one
remote site (`testsite_r_1`, port 5001) - see
`tests/integration/targets/setup_checkmk/defaults/main.yml`.

## Testing a different version or edition

Copy the template and uncomment what you need:

```bash
cp tests/integration/integration_config.yml.template tests/integration/integration_config.yml
```

Then edit `checkmk_var_version` / `checkmk_var_edition` (and, if the
edition needs download credentials, `checkmk_var_download_user` /
`checkmk_var_download_pass`) in that file. `ansible-test` auto-loads it as
extra-vars, which override the role defaults. This file is gitignored —
don't commit it.
