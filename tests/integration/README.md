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

## Podman: raise the task limit

With rootless podman, add this once - without it the tests fail:

```ini
# ~/.config/containers/containers.conf
[containers]
pids_limit = 0
```

Podman's default `pids_limit = 2048` makes `systemd` inside the ansible-test
container cap everything the run starts at 307 tasks, which a Checkmk site
plus its ClickHouse metric backend exceeds. It has to be that file -
`ansible-test` does not pass `CONTAINERS_CONF_OVERRIDE` through to podman. CI
uses Docker, which sets no pids limit.

Symptoms, none of which name the real cause:

- `/bin/sh: 1: Cannot fork`
- a bare Apache `500 Internal Server Error` from the site
- `Couldn't get 512 threads from global thread pool` from ClickHouse

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
