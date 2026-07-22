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

By default this installs Checkmk **2.5.0p9, ultimatemt edition** into a
single container and creates a central site (`testsite`, port 5000) plus
one remote site (`testsite_r_1`, port 5001) — see
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

## Known limitations

- `bakery`, `dcd`, `ldap`, and `lookup_bakery` require a non-community
  edition. They run by default like any other target since the default
  edition is `ultimatemt`. CI's per-target workflow matrix already keeps
  community/`raw` out of their test runs, so no local skip mechanism is
  needed — if you override `checkmk_var_edition` to `community` yourself
  and these fail, that's expected.
- The full suite is expected to run back-to-back cleanly (the
  known cross-target state leaks — `site`'s remote-site probe, the
  `contact_group`/`host_group` alias clash, `ldap`'s missing activation —
  have been fixed). This hasn't been confirmed with a live end-to-end
  `--docker` run yet; see `misc/cross-target_state_issue.txt` for status
  and verification notes.
